"""
Django settings for DDCZ project.
"""

import os, os.path
import sys
from tempfile import gettempdir, mkdtemp

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
)

ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "xoxo"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# WARNING: This affects database migrations. See docs for details
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

DATABASE_IS_SEEDED = False


# Application definition

INSTALLED_APPS = [
    "ddcz.apps.DdczConfig",
    "dragon.apps.DragonConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "graveyard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "ddcz.context_processors.common_variables",
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "cs-CZ"
TIME_ZONE = "Europe/Prague"
USE_I18N = True
USE_L10N = True
USE_TZ = True

APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

GALLERY_MEDIA_ROOT_URL = "https://www.dracidoupe.cz/galerie/"
PHOTOGALLERY_MEDIA_ROOT_URL = "https://www.dracidoupe.cz/fotogalerie/"
USER_ICON_MEDIA_ROOT_URL = "https://www.dracidoupe.cz/ikonky/"
QUEST_MEDIA_ROOT_URL = "http://uploady.dracidoupe.cz/dobrodruzstvi/"


# File Storage, used for Downloady, Dobrodruzstvi etc.
# TODO: Potentially make different backend default,
# see https://github.com/dracidoupe/graveyard/issues/98
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = "uploady.dracidoupe.cz"
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = "uploady.dracidoupe.cz"
AWS_S3_SECURE_URLS = False

# Which email address we are sending transaction emails from
DDCZ_TRANSACTION_EMAIL_FROM = "noreply@example.com"
if ENVIRONMENT == "production":
    EMAIL_FAIL_SILENTLY = False
else:
    EMAIL_FAIL_SILENTLY = True

    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

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


# Hostname for selenium hub for tests. None means running locally
SELENIUM_HUB_HOST = None
# Hostname to which to browser run by selenium hub should connect to
# If none, rely on default Django settings as we are running locally
SELENIUM_PROJECT_HOST = None
SELENIUM_IMPLICIT_WAIT = 10

DISCORD_INVITE_LINK = "https://discord.gg/SnFux2x3Vw"

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
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        }
    },
}
