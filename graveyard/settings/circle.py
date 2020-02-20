import socket

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'circle_test',
        'USER': 'root',
        'HOST': 'db',
        'PASSWORD': 'docker',
        'OPTIONS': {
            'charset': 'latin2'
        },
        'TEST': {
            'NAME': 'circle_test',
            'CHARSET': 'latin2',
        }
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

SELENIUM_HUB_HOST='selenium-hub'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost', 
    socket.gethostname(),
]
