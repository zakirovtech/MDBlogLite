echo "Update https certs..."

certbot renew --webroot \
    --webroot-path /var/www/certbot --non-interactive

if [ $? -ne 0 ]; then
    echo "Certbot cannot find certs, so try to create new..."
    
    if [ "$GRAFANA_STATUS" = "ON" ]; then
        certbot certonly --webroot \
            --webroot-path /var/www/certbot \
             -d "$SITE_DOMAIN" -d "www.$SITE_DOMAIN" -d "service.$SITE_DOMAIN" \
            --email "$ADMIN_EMAIL" --agree-tos --non-interactive
    else
        certbot certonly --webroot \
        --webroot-path /var/www/certbot -d "$SITE_DOMAIN" -d "www.$SITE_DOMAIN" \
        --email "$ADMIN_EMAIL" --agree-tos --non-interactive
    fi
fi
