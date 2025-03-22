echo "Update https certs..."

docker run --env-file ./env/.env certbot renew --webroot \
    --webroot-path /var/www/certbot --non-interactive --quiet

if [ $? -ne 0 ]; then
    echo "Certbot  can not find certs, so try to create new..."
    docker run --env-file ./env/.env certbot certonly --webroot \
        --webroot-path /var/www/certbot -d $SITE_DOMAIN -d www.$SITE_DOMAIN \
        --email $ADMIN_EMAIL --agree-tos --non-interactive
fi
