from .base import *
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(2)
MEDIA_ROOT = PROJECT_DIR.child("load")
STATIC_ROOT = PROJECT_DIR.child("collect_static")
STATICFILES_DIRS = (
    PROJECT_DIR.child("static"),
)
TEMPLATE_DIRS = (
    PROJECT_DIR.child("templates"),
)

# Path to the po|mo files
LOCALE_PATHS = PROJECT_DIR.child('locale')

CKEDITOR_UPLOAD_PATH = PROJECT_DIR.child('ck_uploads')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.inoxtags.db',                      # Or path to database file if using sqlite3.
    }
}'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable("INOXTAGS_DB_NAME"),
        'USER': get_env_variable("INOXTAGS_DB_USER"),
        'PASSWORD': get_env_variable("INOXTAGS_DB_PASSWORD"),
    }
}

ALLOWED_HOSTS = []

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

EMAIL_PORT = get_env_variable("INOXTAGS_EMAIL_PORT")
