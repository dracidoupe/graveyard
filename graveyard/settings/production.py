import os

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
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DATABASE_IS_SEEDED = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ['DB_HOST'],
        'NAME': os.environ['DB_NAME'], # original: dracidoupe_cz
        'USER': os.environ['DB_USERNAME'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'PORT': os.environ['DB_PORT'],
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'charset': 'latin2'
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'ddcz-graveyard',
    }
}

WSGI_APPLICATION = 'graveyard.wsgi.application'

ALLOWED_HOSTS = ['nove.dracidoupe.cz']

# FIXME: Migrate to whitenoise
STATIC_ROOT = '/tmp/'
STATIC_URL = 'https://static.dracidoupe.cz/'

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=False
)


# Security settings
X_FRAME_OPTIONS="DENY"
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True

# Temporary until ACM on production
SECURE_SSL_REDIRECT=False
