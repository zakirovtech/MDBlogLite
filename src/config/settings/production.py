from config.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# DATABASES
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT")
    }
}

# CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('CACHE_DOMAIN')}:{config('REDIS_PORT')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "pool_class": "redis.BlockingConnectionPool",
        }
    }
}

# CSRF
CSRF_TRUSTED_ORIGINS = [
    f"https://{config('SITE_DOMAIN')}",
    f"https://www.{config('SITE_DOMAIN')}",
    "https://127.0.0.1"
]

# SENTRY
SENTRY_STATUS = config("SENTRY_STATUS") == "ON"
if SENTRY_STATUS:
    sentry_sdk.init(
        dsn=config("SENTRY_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        _experiments={
            # Set continuous_profiling_auto_start to True
            # to automatically start the profiler on when
            # possible.
            "continuous_profiling_auto_start": True,
        },
    )
