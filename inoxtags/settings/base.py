#-*- coding:utf-8 -*-
# Django settings for inoxtags project.

import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    '''Get the environment variable or return exeption'''
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Oriol Romero', 'oriol@inoxtags.com'),
)

MANAGERS = ADMINS


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
    ('ca', 'Català'),
    ('es', 'Español'),
    ('en', 'English'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable("INOXTAGS_SECRET_KEY")

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
    'accounts.context_processors.cookies_agreement',
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
    'easy_maps',
    'transmeta',
    'zebra',
    'gunicorn',
    # Apps pròpies del projecte
    'accounts',
    'apps.settings',
    'apps.content_pages',
    'apps.contact',
    'apps.shop',
    'apps.partners',
    'apps.staff',
    'apps.billing',
    'apps.backend_bank_transfer',
    'apps.backend_stripe',
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

# Stripe payments configuration
STRIPE_SECRET = get_env_variable("INOXTAGS_STRIPE_SECRET")
STRIPE_PUBLISHABLE = get_env_variable("INOXTAGS_STRIPE_PUBLISHABLE")


# Django-transmeta, app to have translations in models

TRANSMETA_DEFAULT_LANGUAGE = 'ca'

TRANSMETA_LANGUAGES = (
    ('ca', ugettext('Catalan')),
    ('es', ugettext('Spanish')),
    ('en', ugettext('English')),
)


# Admin site module
GRAPPELLI_ADMIN_HEADLINE = "INOXtags"
GRAPPELLI_ADMIN_TITLE = "INOXtags"

# Configure whether the registration is open or not
REGISTRATION_OPEN = True

# Email configuration
EMAIL_USE_TLS = True
EMAIL_HOST = get_env_variable("INOXTAGS_EMAIL_HOST")
EMAIL_HOST_USER = get_env_variable("INOXTAGS_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_env_variable("INOXTAGS_EMAIL_HOST_PASSWORD")
