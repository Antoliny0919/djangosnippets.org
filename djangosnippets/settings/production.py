from __future__ import absolute_import

import os
from urllib import parse

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa


def env_to_bool(input):
    """
    Must change String from environment variable into Boolean
    defaults to True
    """
    if isinstance(input, str):
        return input not in ("False", "false")
    else:
        return input


DEBUG = env_to_bool(os.environ.get("DEBUG", False))

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN", "")
AWS_PRELOAD_METADATA = True
# AWS_IS_GZIPPED = True
AWS_S3_USE_SSL = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_URL_PROTOCOL = "//:"

SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", False)
SECURE_HSTS_SECONDS = 600
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = env_to_bool(os.environ.get("SESSION_COOKIE_SECURE", True))
SESSION_COOKIE_HTTPONLY = True

# The header Heroku uses to indicate SSL:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MANIFEST_STRICT = False
# Pull the various config info from Heroku.
# Heroku adds some of this automatically if we're using a simple settings.py,
# but we're not and it's just as well -- I like doing this by hand.

# Grab database info
DATABASES = {"default": dj_database_url.config()}


# Make sure urlparse understands custom config schemes.
parse.uses_netloc.append("redis")

# Now do redis and the cache.
redis_url = parse.urlparse(os.environ.get("REDISCLOUD_URL"))
CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "%s:%s" % (redis_url.hostname, redis_url.port),
        "OPTIONS": {
            "PASSWORD": redis_url.password,
            "DB": 0,
            "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
            "CONNECTION_POOL_CLASS_KWARGS": {
                "max_connections": 20,
                "timeout": 20,
            },
        },
    }
}
# Use Sentry for debugging if available.
if "SENTRY_DSN" in os.environ:
    sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN"), integrations=[DjangoIntegration()], send_default_pii=True)


EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = os.environ.get("SENDGRID_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {
        "level": "WARNING",
        "handlers": ["sentry"],
    },
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
    },
    "handlers": {
        "sentry": {
            "level": "ERROR",
            "class": "raven.contrib.django.handlers.SentryHandler",
        },
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "raven": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

SECRET_KEY = os.environ["SECRET_KEY"]

AKISMET_SECRET_API_KEY = os.environ.get("AKISMET_KEY", "")

RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", "")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", "")
RECAPTCHA_USE_SSL = True
