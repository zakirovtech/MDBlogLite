#! bin/bash
if [ "$DJANGO_ENV" = "development" ]; then
    echo "[WARNING] Running in development mode with SQLite database and other debuging settings"

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic

    ./scripts/create_superuser.sh

    python manage.py runserver 0.0.0.0:8000
else
    envsubst '$${SITE_DOMAIN}' < ./config/nginx.template.conf > ./config/nginx.conf
    ./scripts/wait-for-it.sh $DB_HOST:$DB_PORT --timeout=30 --strict -- echo "[INFO] Database is up now"

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput

    ./scripts/create_superuser.sh
    
    gunicorn --bind 0.0.0.0:8000 config.wsgi:application
fi