BASE_DIR = "/app/src"
DEBUG = False
SECRET_KEY = "qwerty"

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
]

PROJECT_APPS = [
    "authentication",
]

INSTALLED_APPS += PROJECT_APPS

STATIC_URL = "/static/"
STATIC_ROOT = "/var/lib/plink/static"
MEDIA_URL = "/media/"
MEDIA_ROOT = "/var/lib/plink/media"


STATICFILES_DIRS = [
    "/app/app/static",
]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
