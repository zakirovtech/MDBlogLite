import sentry_sdk

from config.settings.base import *
from config.utils import is_postgres_available

DEBUG = True

ENABLE_DEBUG_TOOLBAR = config("ENABLE_DEBUG_TOOLBAR", default="0") == "1"

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS.insert(-1, "debug_toolbar")
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1", "localhost", "172.18.0.1"]

ADMIN_ENTRYPOINT = "admin/"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CSRF
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8003",
]

# You can use the code bellow in production settings, when you need to scale
# db servers with master and replicas.
# |
# |
# V

# DATABASES AND REPLICATION
USE_POSTGRES = config("USE_POSTGRES", default="0") == "1"

if not USE_POSTGRES:
    print("[DEBUG] SQLITE3 IS IN USING")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    POSTGRES_HOST = config("POSTGRES_HOST", default="db")
    POSTGRES_PORT = config("POSTGRES_PORT", cast=int, default=5432)
    POSTGRES_DB = config("POSTGRES_DB", default="mdblog")
    POSTGRES_USER = config("POSTGRES_USER", default="mdblog")
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", default="mdblog")

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
            "CONN_MAX_AGE": 60,
        }
    }

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
