
DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dracidoupe_cz',
        'TEST_DATABASE_NAME': 'test_dracidoupe_cz',
        'USER': 'root',
        'PASSWORD': 'xxx',
        'OPTIONS': {
            'charset': 'latin2'
        }
    }
}

