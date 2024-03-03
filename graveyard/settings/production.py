import logging

import os
from .base import BASE_DIR

logger = logging.getLogger(__name__)

DEBUG = False

# This assumes the following environ vars to be configured:
# DJANGO_SECRET_KEY
# SENTRY_DSN
# DB_NAME
# DB_USERNAME
# DB_PASSWORD
# DB_HOST
# DB_PORT

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DATABASE_IS_SEEDED = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ["DB_HOST"],
        "NAME": os.environ["DB_NAME"],  # original: dracidoupe_cz
        "USER": os.environ["DB_USERNAME"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "PORT": os.environ["DB_PORT"],
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            "init_command": "SET NAMES 'latin2';SET sql_mode='STRICT_TRANS_TABLES';",
            "charset": "latin2",
        },
    }
}

if "MEMCACHEDCLOUD_SERVERS" in os.environ:
    logger.info("Using Memcached Cloud servers")

# Use custom and short prefix for cache
KEY_PREFIX = "gy-"
# VERSION variable used for cache versioning is written as part of the release
# see manage.py writerelease command
# VERSION = 1

# See https://devcenter.heroku.com/articles/memcachedcloud#using-memcached-from-python
CACHES = {
    "default": {
        "BACKEND": "django_bmemcached.memcached.BMemcached",
        "LOCATION": os.environ.get("MEMCACHEDCLOUD_SERVERS").split(","),
        "OPTIONS": {
            "username": os.environ.get("MEMCACHEDCLOUD_USERNAME"),
            "password": os.environ.get("MEMCACHEDCLOUD_PASSWORD"),
        },
    }
}


WSGI_APPLICATION = "graveyard.wsgi.application"

ALLOWED_HOSTS = ["www.dracidoupe.cz", "nove.dracidoupe.cz"]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "https://www.dracidoupe.cz/staticfiles/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

## User-uploaded content that is hosted on S3/cloudfront
GALLERY_MEDIA_ROOT_URL = "https://uploady.dracidoupe.cz/galerie/"
PHOTOGALLERY_MEDIA_ROOT_URL = "https://uploady.dracidoupe.cz/fotogalerie/"
USER_ICON_MEDIA_ROOT_URL = "https://uploady.dracidoupe.cz/ikonky/"
QUEST_MEDIA_ROOT_URL = "https://uploady.dracidoupe.cz/dobrodruzstvi/"


import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=False,
)

# Production way of sending email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_FAIL_SILENTLY = False
EMAIL_LINKS_BASE_URI = "https://www.dracidoupe.cz"
EMAIL_HOST = os.environ.get("MAILGUN_SMTP_SERVER", "")
EMAIL_PORT = os.environ.get("MAILGUN_SMTP_PORT", "")
EMAIL_HOST_USER = os.environ.get("MAILGUN_SMTP_LOGIN", "")
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_SMTP_PASSWORD", "")
EMAIL_USE_TLS = True
DDCZ_TRANSACTION_EMAIL_FROM = os.environ.get(
    "DDCZ_TRANSACTION_EMAIL_FROM", "noreply@example.com"
)

# Security settings
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
PASSWORD_RESET_TIMEOUT = 60 * 60 * 3  # 3 hours


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s [%(process)d] [%(levelname)s] "
                + "pathname=%(pathname)s lineno=%(lineno)s "
                + "funcname=%(funcName)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "prod": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "prod",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        }
    },
}
