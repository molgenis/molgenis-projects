# Molgenis Projects

Projects in the **projects** directory use a common theming
format and SCSS build tool. This makes themes more consistent
and easier to maintain. During development, one can use the
Nginx proxy (docker) to apply themes on remote Molgenis
websites.

## Setup

* Start the Nginx proxy; we use the default theme in this example

```bash
# One-time action is to generate an SSL certificate
cd docker/nginx/ssl
./ca_cert.sh localhost
# Sorry, this only works on Archlinux at the moment
# Find out how to apply custom certificates systemwide...
sudo ./ca_system.sh
cd ../../
cp .env.default .env
docker-compose up
```

* In another shell, start the dev tool

```bash
./cli dev
```

> Use the browser [livereload extension](https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei) to autoreload on file-change.

## Adding a new theme

Just copy **theme-3.scss**, **theme-4.scss** and **_variables.scss** from
another theme. Customizable variables are the ones that start with the
**mg-** prefix. Please don't customize Bootstrap variables. Molgenis
transitions from Bootstrap 3 to Bootstrap 4, and still depends on
both. The Molgenis base theme in **scss/molgenis** takes care of
ironing out the differences between both versions.
