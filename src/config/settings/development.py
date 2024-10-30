from config.settings.base import *
import sentry_sdk

DEBUG = True

INSTALLED_APPS.insert(-1, "debug_toolbar")
MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1", "localhost", "172.18.0.1"]

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ADMIN_ENTRYPOINT = "admin/"

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}

# CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://cache:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "pool_class": "redis.BlockingConnectionPool",
        }
    }
}

# CELERY
CELERY_BROKER_URL = 'redis://cache:6379/0'

# SENTRY
SENTRY_STATUS = False
