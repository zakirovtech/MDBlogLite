from config.settings.base import *
import sentry_sdk

DEBUG = True
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
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'cache'
    }
}   

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
