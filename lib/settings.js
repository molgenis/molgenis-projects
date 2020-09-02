import {__dirname} from './utils.js'
import fs from 'fs-extra'
import path from 'path'
import ini from 'ini'


export default async() => {
    const settings = {dir: {base: path.resolve(path.join(__dirname, '../'))}}
    settings.dir.node = path.resolve(path.join(settings.dir.base, 'node_modules'))
    settings.dir.theme = path.resolve(path.join(settings.dir.base, 'projects'))
    const defaults = ini.parse((await fs.readFile(path.join(settings.dir.base, 'docker', '.env'), 'utf8')))
    Object.assign(settings, defaults)

    return settings
}