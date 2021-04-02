DEBUG = True

ALLOWED_HOSTS = ["yourcomputer", "yourcomputer.local", "localhost", "127.0.0.1", "::1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "dracidoupe_cz",
        "USER": "root",
        "HOST": "db",
        "PASSWORD": "docker",
        "OPTIONS": {"charset": "latin2"},
        "TEST": {
            "NAME": "test_dracidoupe_cz",
            "CHARSET": "latin2",
        },
    }
}
