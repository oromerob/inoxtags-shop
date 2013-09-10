#-*- coding:utf-8 -*-
# Local settings for inoxtags project

import os
SITE_ROOT = os.path.dirname(os.path.relpath(__file__))

# Path to the po|mo files
LOCALE_PATHS = (os.path.join(SITE_ROOT, 'locale'),)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.inoxtags.db',                      # Or path to database file if using sqlite3.
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'load')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'collect_static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8b#zwq#3c$qfz$r%$p3*=a!0ur0*!u+v^7ym%p8e%@artcj#m='

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

# CkEditor configuration
CKEDITOR_UPLOAD_PATH = os.path.join(SITE_ROOT, 'ck_uploads')

# Email configuration
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '13.oriol@gmail.com'
EMAIL_HOST_PASSWORD = 'nponuzzyarbcsjcz'
EMAIL_PORT = 587

"""
Configurable settings via Admin site:
"""
from apps.settings.models import ProjectSettings

try:
    settings = ProjectSettings.objects.filter(is_active=True).get()

    # Admin site module
    GRAPPELLI_ADMIN_HEADLINE = settings.name
    GRAPPELLI_ADMIN_TITLE = settings.name

    # Configure whether the registration is open or not
    REGISTRATION_OPEN = settings.registration_open

except:
    settings = None
