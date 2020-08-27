import {__dirname} from './utils.js'
import fs from 'fs-extra'
import path from 'path'
import rc from 'rc'


export default async() => {
    const settings = {dir: {base: path.resolve(path.join(__dirname, '../'))}}
    settings.dir.node = path.resolve(path.join(settings.dir.base, 'node_modules'))
    const defaults = JSON.parse(await fs.readFile(path.join(settings.dir.base, '.mg-projects.defaults'), 'utf8'))

    Object.assign(settings, rc('mg-projects', defaults))

    return settings
}