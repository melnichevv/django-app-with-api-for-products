from .development import *  # noqa

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": ("%(levelname)s %(asctime)s %(module)s %(process)d " "%(thread)d %(message)s")},
        "simple": {"format": "%(module)s %(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "simple"},
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
    },
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "django.db.backends": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "": {"handlers": ["console"], "propagate": False, "level": get_env("LOGGING_LEVEL_ROOT", "INFO")},
        # "base": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}
