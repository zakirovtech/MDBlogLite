export NGINX_CONFIG=/etc/nginx/conf.d/default.conf

cat <<EOL > $NGINX_CONFIG
server {
    listen 80;
    server_name $SITE_DOMAIN;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

}
EOL
