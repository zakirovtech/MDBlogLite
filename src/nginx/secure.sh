#!/usr/bin/env bash
set -euo pipefail

set -a
source <(grep -E '^[A-Z_][A-Z0-9_]*=' ./env/.env)
set +a

: "${SITE_DOMAIN:?SITE_DOMAIN is not set in ./env/.env}"

CONF_DIR="/opt/nginx/conf.d"
NGINX_CONFIG="${CONF_DIR}/${SITE_DOMAIN}.conf"

mkdir -p "$CONF_DIR"

tmp="$(mktemp)"
cat > "$tmp" <<EOL
# ${SITE_DOMAIN} (generated)

server {
    listen 80;
    listen [::]:80;
    server_name ${SITE_DOMAIN} www.${SITE_DOMAIN};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    llisten 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name ${SITE_DOMAIN} www.${SITE_DOMAIN};

    ssl_certificate /etc/nginx/ssl/live/${SITE_DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/${SITE_DOMAIN}/privkey.pem;

    # Optional hardening (safe defaults)
    ssl_protocols TLSv1.2 TLSv1.3;

    location /static/ {
        alias /${APP}/static/;
    }

    location /media/ {
        alias /${APP}/media/;
    }

    location / {
        proxy_pass http://${DOCKER_SERVICE_NAME}:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
EOL

# Idempotent: no change if already identical
if [ -f "$NGINX_CONFIG" ] && cmp -s "$tmp" "$NGINX_CONFIG"; then
  echo "OK: $NGINX_CONFIG already up-to-date"
  rm -f "$tmp"
  exit 0
fi

# Optional backup
if [ -f "$NGINX_CONFIG" ]; then
  cp -a "$NGINX_CONFIG" "${NGINX_CONFIG}.bak"
fi

mv "$tmp" "$NGINX_CONFIG"
echo "Updated: $NGINX_CONFIG"

echo "Delete old certbot-http config"
rm -f "/opt/nginx/conf.d/certbot-http-${SITE_DOMAIN}.conf"
