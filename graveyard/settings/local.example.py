import os
import os.path
from tempfile import gettempdir, mkdtemp


DEBUG = True
OVERRIDE_SELENIUM_DEBUG = True

ALLOWED_HOSTS = ["yourcomputer", "yourcomputer.local", "localhost", "127.0.0.1", "::1"]
EMAIL_LINKS_BASE_URI = "http://localhost:8080"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "dracidoupe_cz",
        "USER": "root",
        "HOST": "db",
        "PASSWORD": "docker",
        "OPTIONS": {
            "init_command": "SET NAMES 'latin2';SET sql_mode='STRICT_TRANS_TABLES';",
            "charset": "latin2",
        },
        "TEST": {
            "NAME": "test_dracidoupe_cz",
            "CHARSET": "latin2",
        },
    }
}

# Test speedup
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# You can keep the local cache as specified in base.py for production-like behavior
# Use this is you absolutely don't want anything to be cached, but be careful
# since you may inadvertedly introduce bugs that will only show up in production!
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Store all emails in a freshly created directory in the system's temporary directory
maildir = os.path.join(gettempdir(), "ddcz-devserver-emails")
if not os.path.exists(maildir):
    try:
        os.mkdir(maildir)
    except BaseException:
        maildir = None
elif not os.access(maildir, os.W_OK):
    maildir = None

if not maildir:
    maildir = mkdtemp(prefix="ddcz-devserver-emails-")

EMAIL_FILE_PATH = maildir


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s [%(process)d] [%(levelname)s] "
                + "pathname=%(pathname)s lineno=%(lineno)s "
                + "funcname=%(funcName)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        # "null": {
        #     "level": "DEBUG",
        #     "class": "logging.NullHandler",
        # },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "verbose",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.db.backends": {
            "level": "INFO",
            "handlers": ["console"],
        },
    },
}
