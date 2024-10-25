certbot certonly --webroot --webroot-path /var/www/certbot \
    -d $SITE_DOMAIN -d www.$SITE_DOMAIN \
    --email $ADMIN_EMAIL \
    --agree-tos --non-interactive
