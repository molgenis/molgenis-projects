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

## Configuration

The configuration for molgenis-projects is located in **docker/.env**. It
has the following options:

```bash
# No need to change this; used to make docker containers unique per project
COMPOSE_PROJECT_NAME=mg_projects
```

```bash
# Determines which services are started; e.g. only the Nginx proxy
COMPOSE_FILE=dc-proxy.yml
# Nginxm proxy + molgenis services; use when you need to test changes
# in Molgenis itself from IntelliJ.
COMPOSE_FILE=dc-proxy.yml:dc-mg-services.yml
# The whole Molgenis stack; useful to test a deployment
COMPOSE_FILE=dc-proxy.yml:dc-mg-services.yml:dc-mg.yml
```

```bash
# Use external Molgenis instance when only using the Nginx proxy
MG_HOST=https://master.dev.molgenis.org
# Use docker name in combination with running the whole Molgenis stack.
MG_HOST=http://molgenis:8080
```

```bash
# Static fileserver root directory
MG_PUBLISH_ROOT=/home/molgenis/molgenis/css
# Remote SSH host
MG_PUBLISH_HOST=static.molgenis.org
# Path to your private SSH key
MG_PUBLISH_KEY=/home/user/.ssh/id_rsa
# SSH Daemon port
MG_PUBLISH_PORT=50666
# SSH user to login with
MG_PUBLISH_USER=molgenis
# CSS Versioning directory; use minor semver releases only?
MG_PUBLISH_VERSION=4.5
```

```bash
# Which theme to watch and/or build from the /projects dir
MG_THEME=default
# The proxied Molgenis CSS file to watch for changes
MG_WATCHFILE=bootstrap-molgenis-blue.min.css
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

## Create A New Theme

Copy **theme-3.scss**, **theme-4.scss** and **_variables.scss** from
another theme. Customizable variables are the ones that start with the
**mg-** prefix. Please don't customize Bootstrap variables. Molgenis
transitions from Bootstrap 3 to Bootstrap 4, and still depends on
both. The Molgenis base theme in **scss/molgenis** takes care of
ironing out the differences between both versions.