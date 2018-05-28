
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dracidoupe_cz',
        'TEST_DATABASE_NAME': 'circle_test',
        'USER': 'root',
        'HOST': '127.0.0.1',
        'PASSWORD': '',
        'OPTIONS': {
            'charset': 'latin2'
        }
    }
}

