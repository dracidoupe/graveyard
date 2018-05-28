

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xoxo, but longer and on production'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dracidoupe_cz',
        'OPTIONS': {
            'charset': 'latin2'
        }
    }
}


WSGI_APPLICATION = 'graveyard.wsgi.application'

ALLOWED_HOSTS = []
