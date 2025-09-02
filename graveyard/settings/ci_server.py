import socket

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ddcz",
        "USER": "postgres",
        "HOST": "db",
        "PASSWORD": "docker",
        "PORT": "5432",
        "TEST": {
            "NAME": "test_ddcz",
        },
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

SELENIUM_HUB_HOST = "selenium-hub"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    socket.gethostname(),
]
