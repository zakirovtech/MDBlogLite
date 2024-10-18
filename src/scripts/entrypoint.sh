#! bin/bash

chmod +x ./scripts/wait-for-it.sh
./scripts/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up now"

python manage.py makemigrations --noinput
python manage.py migrate --noinput

chmod +x ./scripts/create_superuser.sh
./scripts/create_superuser.sh

python manage.py runserver 0.0.0.0:8080