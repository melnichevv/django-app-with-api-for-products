from .development import *  # noqa

DEBUG = False

DATABASES["default"]["CONN_MAX_AGE"] = 600  # noqa

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_URL = "/static/"
ASSETS_URL = "/static/"
MEDIA_URL = "/media/"
