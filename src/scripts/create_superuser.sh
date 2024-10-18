echo "from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$ADMIN_USERNAME').exists():
    User.objects.create_superuser('$ADMIN_USERNAME', '$ADMIN_EMAIL', '$ADMIN_PASSWORD'); print('Superuser is created.')" | python manage.py shell
