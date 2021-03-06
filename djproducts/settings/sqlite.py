"""Use Sqlite database for running Django checks that do not require a full db."""
from .test import *  # noqa: F401, F403

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
