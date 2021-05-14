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

# You can keep the local cache as specified in base for production-like behavior
# Use this is you absolutely don't want anything to be cached
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
