#!/usr/bin/env bash
set -euo pipefail

set -a
. env/.env
set +a

: "${SITE_DOMAIN:?SITE_DOMAIN is not set in env/.env}"

CONF_DIR="/opt/nginx/conf.d"
NGINX_CONFIG="${CONF_DIR}/certbot-http-${SITE_DOMAIN}.conf"

mkdir -p "$CONF_DIR"

tmp="$(mktemp)"
cat > "$tmp" <<EOL
server {
    listen 80;
    server_name ${SITE_DOMAIN} www.${SITE_DOMAIN};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
}
EOL

# Idempotent: if file exists and is identical -> keep as is
if [ -f "$NGINX_CONFIG" ] && cmp -s "$tmp" "$NGINX_CONFIG"; then
  echo "OK: $NGINX_CONFIG already up-to-date"
  rm -f "$tmp"
  exit 0
fi

# Optional backup of old version
if [ -f "$NGINX_CONFIG" ]; then
  cp -a "$NGINX_CONFIG" "${NGINX_CONFIG}.bak"
fi

# Atomic replace
mv "$tmp" "$NGINX_CONFIG"
echo "Updated: $NGINX_CONFIG"
