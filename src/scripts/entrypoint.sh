#! bin/bash
if [ "$DJANGO_ENV" = "development" ]; then
    echo "[WARNING] Running in development mode with SQLite database and other debuging settings"

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    ./scripts/create_superuser.sh
    python manage.py runserver 0.0.0.0:8000
else
    # chmod +x ./scripts/wait-for-it.sh
    ./scripts/wait-for-it.sh $DB_HOST:$DB_PORT --timeout=30 --strict -- echo "[INFO] Database is up now"

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput

    # chmod +x ./scripts/create_superuser.sh
    ./scripts/create_superuser.sh

    python manage.py runserver 0.0.0.0:8080
fi