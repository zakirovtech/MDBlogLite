set -a

. env/.env

set +a

touch nginx/nginx.conf

export NGINX_CONFIG=./nginx/nginx.conf

cat <<EOL > $NGINX_CONFIG
server {
    listen 80;
    server_name $SITE_DOMAIN www.$SITE_DOMAIN;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
}
EOL
