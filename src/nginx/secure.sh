set -a

. ./env/.env

set +a

export NGINX_CONFIG="/etc/nginx/conf.d/$SITE_DOMAIN.conf"

cat <<EOL > $NGINX_CONFIG
server {
    listen 80;
    listen [::]:80;
    server_name _;
    
    return 444;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name _;

    ssl_certificate /etc/nginx/ssl/live/$SITE_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/$SITE_DOMAIN/privkey.pem;

    return 444;
}

server {
    listen 80;
    listen [::]:80;
    server_name $SITE_DOMAIN www.$SITE_DOMAIN;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name $SITE_DOMAIN www.$SITE_DOMAIN;

    ssl_certificate /etc/nginx/ssl/live/$SITE_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/$SITE_DOMAIN/privkey.pem;

    location /static/ {
        alias /app/static/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL
