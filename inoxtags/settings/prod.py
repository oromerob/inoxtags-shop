from .base import *
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(2)
MEDIA_ROOT = PROJECT_DIR.ancestor(2).child("inoxtags_media")
STATIC_ROOT = PROJECT_DIR.ancestor(2).child("inoxtags_static")
STATICFILES_DIRS = (
    PROJECT_DIR.child("static"),
)
TEMPLATE_DIRS = (
    PROJECT_DIR.child("templates")
)

# Path to the po|mo files
LOCALE_PATHS = PROJECT_DIR.child('locale')

CKEDITOR_UPLOAD_PATH = PROJECT_DIR.ancestor(2).child('inoxtags_media').child('ck_uploads')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable("INOXTAGS_DB_NAME"),
        'USER': get_env_variable("INOXTAGS_DB_USER"),
        'PASSWORD': get_env_variable("INOXTAGS_DB_PASSWORD"),
    }
}

ALLOWED_HOSTS = [".inoxtags.com",]

MEDIA_URL = 'https://www.inoxtags.com/media/'
STATIC_URL = 'https://www.inoxtags.com/static/'

DEFAULT_FROM_EMAIL = get_env_variable("INOXTAGS_DEFAULT_FROM_EMAIL")
SERVER_EMAIL = get_env_variable("INOXTAGS_SERVER_EMAIL")
