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
            ],
            outFile: target.css,
            sourceMap: !settings.optimize,
            sourceMapContents: true,
            sourceMapEmbed: false,
        }, async function(err, sassObj) {
            if (err) reject(err.formatted)
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
    await Promise.all([
        tasks.scss.start(),
    ])
})


/**
 * Some Molgenis views use Bootstrap 3, others use Bootstrap 4.
 * The result should look the same with the least amount of
 * customization.
 */
tasks.scss = new Task('scss', async function() {
    let scssDir, themeName
    // No entrypoint; build default theme.
    if (this.ep) {
        scssDir = path.dirname(this.ep.raw)
        themeName = path.join(scssDir, '..').replace(settings.dir.base, '').replace(path.sep, '')
    } else {
        scssDir = path.join(settings.dir.base, settings.theme, 'scss')
        themeName = settings.theme
    }

    await Promise.all([
        sassRender(path.join(scssDir, 'theme-3.scss'), `${themeName}_bootstrap3.css`),
        sassRender(path.join(scssDir, 'theme-4.scss'), `${themeName}_bootstrap4.css`)
    ])
})


tasks.watch = new Task('watch', async function() {
    return new Promise((resolve) => {
        var app = connect()
        app.use(tinylr.middleware({app}))
        app.listen({host: settings.dev.host, port: settings.dev.port}, () => {
            this.log(`development server listening: ${chalk.grey(`${settings.dev.host}:${settings.dev.port}`)}`)
            resolve()
        })

        chokidar.watch(path.join(settings.dir.base, '**', 'scss', '*.scss')).on('change', async(file) => {
            await tasks.scss.start(file)
            tinylr.changed(settings.livereload)
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
        .option('theme', {alias: 't', description: `Selected theme [${settings.theme}]`, type: 'string'})
        .option('livereload', {alias: 'l', default: 'app.css', description: 'CSS theme file to reload', type: 'string'})
        .option('optimize', {alias: 'o', default: false, description: 'Optimize for production', type: 'boolean'})
        .middleware(async(argv) => {
            if (!settings.version) {
                settings.version = JSON.parse((await fs.readFile(path.join(settings.dir.base, 'package.json')))).version
            }

            tasks.watch.log(`theme: ${chalk.cyan(settings.theme)}`)
            if (argv._.includes('watch')) {
                tasks.watch.log(`proxy css to reload: ${chalk.cyan(argv.livereload)}`)
            }

            settings.optimize = argv.optimize
            // Could be a mapping later.
            settings.livereload = argv.livereload
            if (settings.optimize) {
                tasks.watch.log(`build optimization: ${chalk.green('enabled')}`)
            } else {
                tasks.watch.log(`build optimization: ${chalk.red('disabled')}`)
            }
        })

        .command('build', `build package`, () => {}, () => {tasks.build.start()})
        .command('config', 'list build config', () => {}, () => buildInfo(cli))
        .command('scss', 'compile stylesheets (SCSS)', () => {}, () => {tasks.scss.start()})
        .command('watch', `development modus`, () => {}, () => {tasks.watch.start()})
        .demandCommand()
        .help('help')
        .showHelpOnFail(true)
        .argv


})()



