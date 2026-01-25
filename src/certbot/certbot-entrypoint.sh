echo "Update https certs..."
CERT_DIR="/etc/letsencrypt/live/${SITE_DOMAIN}"

if [ ! -f "${CERT_DIR}/fullchain.pem" ] || [ ! -f "${CERT_DIR}/privkey.pem" ]; then
    echo "No certs found, creating new..."

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
else
  echo "Certs exist, trying renew..."

  certbot renew --webroot \
    --webroot-path /var/www/certbot --non-interactive

fi
