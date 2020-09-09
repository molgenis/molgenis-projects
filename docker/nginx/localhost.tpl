server {
  listen 80 default_server;
  server_name localhost;

  access_log /dev/stdout;
  error_log /dev/stdout info;

  location @handle_redirect {
      # drop routing information from urls that do not start with `/dist/`
      rewrite ^/([^/]*)/([^/]*)/(?!dist/).*$ /$1/$2 last;
      proxy_intercept_errors on;
      error_page 301 302 307 = @handle_redirect;
      set $frontend_host 'https://unpkg.com';
      set $saved_redirect_location '$upstream_http_location';

      proxy_pass $frontend_host$saved_redirect_location;
      # Do not cache these redirects too long
      expires 10m;
  }

  location /@molgenis-experimental/molgenis-app-lifelines-webshop/ {
      proxy_pass https://unpkg.com/@molgenis-experimental/molgenis-app-lifelines-webshop@2.5.2/;
      proxy_intercept_errors on;
      recursive_error_pages on;
      error_page 301 302 307 = @handle_redirect;
  }

  location /@molgenis-experimental/ {
      proxy_pass https://unpkg.com/@molgenis-experimental/;
      proxy_intercept_errors on;
      recursive_error_pages on;
      error_page 301 302 307 = @handle_redirect;
  }

  # HACK: Override a hardcoded theme from de2
  location /@molgenis-ui/data-explorer/dist/bootstrap-molgenis-blue.min.css {
      add_header Last-Modified $date_gmt;
      add_header Cache-Control 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';
      root /usr/share/nginx/html/;
      rewrite ^ /${MG_THEME}/css/mg-${MG_THEME}-4.css break;
  }

   # HACK: Override a legacy hardcoded Bootstrap 3 theme with our own (login)
  location /css/bootstrap.min.css {
      add_header Last-Modified $date_gmt;
      add_header Cache-Control 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';
      root /usr/share/nginx/html/;
      rewrite ^ /${MG_THEME}/css/mg-${MG_THEME}-3.css break;
  }

  location /@molgenis-ui/ {
      proxy_pass https://unpkg.com/@molgenis-ui/;
      proxy_intercept_errors on;
      recursive_error_pages on;
      error_page 301 302 307 = @handle_redirect;
  }

  location /css/bootstrap-3/${MG_WATCHFILE} {
      add_header Last-Modified $date_gmt;
      add_header Cache-Control 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';
      root /usr/share/nginx/html/;
      rewrite ^ /${MG_THEME}/css/mg-${MG_THEME}-3.css break;
  }


  location /css/bootstrap-4/mg-${MG_THEME}-3.css.map {
    add_header Last-Modified $date_gmt;
    add_header Cache-Control 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';
    root /usr/share/nginx/html/;
    rewrite ^ /${MG_THEME}/css/mg-${MG_THEME}-3.css.map break;
  }

  location /css/bootstrap-4/${MG_WATCHFILE} {
      add_header Last-Modified $date_gmt;
      add_header Cache-Control 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';
      root /usr/share/nginx/html/;
      rewrite ^ /${MG_THEME}/css/mg-${MG_THEME}-4.css break;
  }

  location /css/bootstrap-4/mg-${MG_THEME}-4.css.map {
    add_header Last-Modified $date_gmt;
    add_header Cache-Control 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';
    root /usr/share/nginx/html/;
    rewrite ^ /${MG_THEME}/css/mg-${MG_THEME}-4.css.map break;
  }

  location / {
      proxy_buffers 4 32k;
      proxy_pass ${MG_HOST};
      proxy_ssl_session_reuse on;
  }
}