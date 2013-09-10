#-*- coding:utf-8 -*-
# Django settings for inoxtags project.

import os
SITE_ROOT = os.path.dirname(os.path.relpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Oriol Romero', 'oriol@inoxtags.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.inoxtags.db',                      # Or path to database file if using sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ca'

ugettext = lambda s: s

LANGUAGES = (
    ('ca', ugettext('Catalan')),
    ('es', ugettext('Spanish')),
    ('en', ugettext('English')),
)

# Path to the po|mo files
LOCALE_PATHS = (os.path.join(SITE_ROOT, 'locale'),)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

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

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8b#zwq#3c$qfz$r%$p3*=a!0ur0*!u+v^7ym%p8e%@artcj#m='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

# Linies per permetre usar el request en els templates:
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'apps.settings.context_processors.project',
    'accounts.context_processors.auth_form',
    'apps.shop.context_processors.cart_context',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'inoxtags.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'inoxtags.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'autoslug',     # App que permet generar slugs automàticament en els models.
    'registration',     # App senzilla que aporta les funcionalitats bàsiques d'un mòdul d'autenticació.
    'south',    # App que permet la modificació dels models.
    'ckeditor',     # App per tenir accés a utilitzar el CKEditor a l'editar des del lloc de l'administrador
    'braintree',    # App per tramitar els pagaments
    'easy_maps',
    'transmeta',
    # Apps pròpies del projecte
    'accounts',
    'apps.settings',
    'apps.content_pages',
    'apps.contact',
    'apps.shop',
    'apps.payments',
    'apps.checkout',
    'apps.partners',
    'apps.staff',
    # Mòdols d'administració
    'grappelli',    # App que canvia l'aparença de l'administrador i que se suposa que aporta funcions de CMS
    'django.contrib.admin',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Custom user model
AUTH_USER_MODEL = 'accounts.InoxUser'

# Custom login redirect url
LOGIN_REDIRECT_URL = '/'

# Email configuration
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '13.oriol@gmail.com'
EMAIL_HOST_PASSWORD = 'nponuzzyarbcsjcz'
EMAIL_PORT = 587

# CkEditor configuration
CKEDITOR_UPLOAD_PATH = os.path.join(SITE_ROOT, 'ck_uploads')

# Braintree payments configuration
import braintree

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    "rhkhwbt6g8tv5wq2",
    "c8fs4545j7bnmt9m",
    "e03a41b86facddf7fe8bf6ad3b05ccf4"
)

# Django-transmeta, app to have translations in models

TRANSMETA_DEFAULT_LANGUAGE = 'ca'

TRANSMETA_LANGUAGES = (
    ('ca', ugettext('Catalan')),
    ('es', ugettext('Spanish')),
    ('en', ugettext('English')),
)


# Configurable settings via Admin site:
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
