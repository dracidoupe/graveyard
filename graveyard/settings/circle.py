
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ddcz',
        'TEST_DATABASE_NAME': 'circle_test',
        'USER': 'root',
        'HOST': 'db',
        'PASSWORD': 'docker',
        'OPTIONS': {
            'charset': 'latin2'
        }
    }
}

