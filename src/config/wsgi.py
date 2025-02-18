"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.settings.base import config

if config("DJANGO_ENV") == "production":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.production"
    )
else:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.development"
    )

application = get_wsgi_application()
