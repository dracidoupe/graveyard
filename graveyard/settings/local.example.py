DEBUG = True


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
