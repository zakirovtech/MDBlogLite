import sentry_sdk

from config.settings.base import *
from config.utils import is_postgres_available

DEBUG = True

INSTALLED_APPS.insert(-1, "debug_toolbar")
MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1", "localhost", "172.18.0.1"]
ADMIN_ENTRYPOINT = "admin/"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CSRF
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8080",
]

# You can use the code bellow in production settings, when you need to scale
# db servers with master and replicas.
# |
# |
# V

# DATABASES AND REPLICATION
db_creds = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": config("POSTGRES_DB"),
    "USER": config("POSTGRES_USER"),
    "PASSWORD": config("POSTGRES_PASSWORD"),
    "HOST": "192.168.0.100",  # localhost MasterDB
    "PORT": config("DB_PORT"),
}

SQLITE3 = None

if not is_postgres_available(credentials=db_creds):
    print("[DEBUG] SQLITE3 IS IN USING")

    SQLITE3 = True

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB"),
            "USER": config("POSTGRES_USER"),
            "PASSWORD": config("POSTGRES_PASSWORD"),
            "HOST": "192.168.0.100",  # localhost MasterDB
            "PORT": config("DB_PORT"),
        },
        "replica": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB"),
            "USER": config("POSTGRES_USER"),
            "PASSWORD": config("POSTGRES_PASSWORD"),
            "HOST": "192.168.0.101",  # localhost ReplicaDB1
            "PORT": config("DB_PORT"),
        },
    }

if not SQLITE3:
    DATABASE_ROUTERS = ["config.dbrouting.ReadWriteRouter"]

# CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://cache:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "pool_class": "redis.BlockingConnectionPool",
        },
    }
}

# CELERY
CELERY_BROKER_URL = "redis://cache:6379/0"

# SENTRY
SENTRY_STATUS = False

# RECAPTCHA
SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]
