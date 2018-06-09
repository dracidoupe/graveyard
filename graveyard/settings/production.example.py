
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xoxo, but longer and on production'

DATABASE_IS_SEEDED = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dracidoupe_cz',
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

STATIC_ROOT = '/var/www/dracidoupe.cz/www_root/static/htdocs/'

STATIC_URL = 'https://static.dracidoupe.cz/'

# Security settings
X_FRAME_OPTIONS="DENY"
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
