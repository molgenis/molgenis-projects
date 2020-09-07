# Molgenis Projects

Projects in the **projects** directory use a common theming
format and SCSS build tool. This makes themes more consistent
and easier to maintain. During development, one can use the
Nginx proxy (docker) to apply themes on remote Molgenis
websites.

## Prerequisites

* [Visual Studio Code](https://code.visualstudio.com/docs/setup/mac)
* [Node.js](https://nodejs.org/dist/v14.9.0/node-v14.9.0.pkg)
* [Yarn](https://classic.yarnpkg.com/en/docs/install/#mac-stable)
* [Docker](https://docs.docker.com/docker-for-mac/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)

## Usage

```bash
git clone git@github.com:molgenis/molgenis-projects.git
cd molgenis-projects
yarn
# Set the config file
cp docker/.env.default docker/.env
# Build the selected theme (MG_THEME in .env)
yarn build
# Build all themes in /projects
yarn build-all
# Publish the selected theme
yarn publish
# Publish all themes
yarn publish-all
```

## Development

* Start the Nginx proxy; we use the default theme in this example

```bash
docker-compose up nginx
```

* In another shell, start the dev tool

```bash
yarn dev
```

> Use the browser [livereload extension](https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei) to autoreload on file-change.

## Adding a new theme

Copy **theme-3.scss**, **theme-4.scss** and **_variables.scss** from
another theme. Customizable variables are the ones that start with the
**mg-** prefix. Please don't customize Bootstrap variables. Molgenis
transitions from Bootstrap 3 to Bootstrap 4, and still depends on
both. The Molgenis base theme in **scss/molgenis** takes care of
ironing out the differences between both versions.
