#!/usr/bin/env node
import _ from 'lodash'
import {buildInfo} from './lib/utils.js'
import chalk from 'chalk'
import chokidar from 'chokidar'
import CleanCSS from 'clean-css'
import connect from 'connect'
import fs from 'fs-extra'
import globImporter from 'node-sass-glob-importer'
import loadSettings from './lib/settings.js'
import notifier from 'node-notifier'
import path from 'path'
import sass from 'node-sass'
import Task from './lib/task.js'
import tinylr from 'tiny-lr'
import yargs from 'yargs'


const cleanCSS = new CleanCSS({level: 2, returnPromise: true, sourceMap: true})
let settings
const tasks = {}


function sassRender(themeFile, cssEntry) {
    const cssDir = path.join(path.dirname(themeFile), '..', 'css')
    let target = {
        css: path.join(cssDir, cssEntry),
        map: path.join(cssDir, `${cssEntry}.map`),
    }

    return new Promise((resolve, reject) => {
        sass.render({
            file: themeFile,
            importer: globImporter(),
            includePaths: [
                'node_modules',
                'node_modules/bootstrap-sass/assets/stylesheets',
                'scss',
            ],
            outFile: target.css,
            sourceMap: !settings.optimize,
            sourceMapContents: true,
            sourceMapEmbed: false,
        }, async function(err, sassObj) {
            if (err) {
                notifier.notify({
                    title: 'SCSS Error',
                    message: err.formatted
                })
                reject(err.formatted)

            }
            let cssRules
            const promises = []
            if (settings.optimize) {
                cssRules = (await cleanCSS.minify(sassObj.css)).styles
            } else {
                cssRules = sassObj.css
                promises.push(fs.writeFile(target.map, sassObj.map))
            }

            promises.push(fs.writeFile(target.css, cssRules))
            await Promise.all(promises)
            resolve({size: cssRules.length})
        })
    })
}


tasks.build = new Task('build', async function() {
    if (settings.all) {
        const themes = await fs.readdir(settings.dir.theme)
        await Promise.all(themes.map((theme) => {
            tasks.scss.start(theme)
        }))
    } else {
        await tasks.scss.start(settings.MG_THEME)
    }
})


/**
 * Some Molgenis views use Bootstrap 3, others use Bootstrap 4.
 * The result should look the same with the least amount of
 * customization.
 */
tasks.scss = new Task('scss', async function() {
    let theme
    this.ep.raw ? theme = this.ep.raw : settings.dir.theme
    const themeDir = path.join(settings.dir.theme, theme, 'scss')
    await Promise.all([
        sassRender(path.join(themeDir, 'theme-3.scss'), `mg-${theme}-3.css`),
        sassRender(path.join(themeDir, 'theme-4.scss'), `mg-${theme}-4.css`)
    ])
})


tasks.dev = new Task('dev', async function() {
    await tasks.build.start()
    return new Promise((resolve) => {
        var app = connect()
        app.use(tinylr.middleware({app}))
        app.listen({host: '127.0.0.1', port: 35729}, () => resolve)

        chokidar.watch([
            path.join(settings.dir.theme, settings.MG_THEME, '**', 'scss', '*.scss'),
            path.join(settings.dir.base, 'scss', '**', '*.scss')
        ]).on('change', async(file) => {
            await tasks.scss.start(file)
            tinylr.changed(settings.MG_WATCHFILE)
        })
    })
})


;(async() => {
    settings = await loadSettings()

    const cli = {
        // eslint-disable-next-line no-console
        log(...args) {console.log(...args)},
        settings,
    }

    yargs
        .usage('Usage: $0 [task]')
        .detectLocale(false)
        .option('all', {default: false, description: 'Apply to all themes', type: 'boolean'})
        .option('optimize', {alias: 'o', default: false, description: 'Optimize for production', type: 'boolean'})
        .middleware(async(argv) => {
            if (!settings.version) {
                settings.version = JSON.parse((await fs.readFile(path.join(settings.dir.base, 'package.json')))).version
            }

            tasks.dev.log(`\r\n${chalk.bold('THEME:')} ${chalk.cyan(settings.MG_THEME)}`)
            if (argv._.includes('dev')) {
                tasks.dev.log(`${chalk.bold('WATCH FILE:')} ${chalk.cyan(settings.MG_WATCHFILE)}`)
            }

            settings.all = argv.all
            settings.optimize = argv.optimize
            // Could be a mapping later.
            tasks.dev.log(`${chalk.bold('MINIFY:')} ${chalk.grey(settings.optimize)}\r\n`)
        })

        .command('build', `build project files`, () => {}, () => {tasks.build.start()})
        .command('config', 'list build config', () => {}, () => buildInfo(cli))
        .command('scss', `build stylesheets for ${settings.MG_THEME}`, () => {}, () => {tasks.scss.start()})
        .command('dev', `development mode`, () => {}, () => {tasks.dev.start()})
        .demandCommand()
        .help('help')
        .showHelpOnFail(true)
        .argv
})()



