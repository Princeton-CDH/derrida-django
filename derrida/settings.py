"""
Django settings for derrida project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/


# Application definition
INSTALLED_APPS = [
    'dal',
    'dal_select2',
    # dal and dal_select2 must be added before grappelli
    'grappelli',
    'compressor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django_cas_ng',
    'sortedm2m',
    'pucas',
    'djiffy',
    'annotator_store',
    'viapy',
    'haystack',
    'widget_tweaks',
    # local apps
    'derrida.apps.DerridaConfig',
    'derrida.books',
    'derrida.places',
    'derrida.people',
    'derrida.footnotes',
    'derrida.common',
    'derrida.interventions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

ROOT_URLCONF = 'derrida.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [
            os.path.join(BASE_DIR, "templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'derrida.context_extras',
                'derrida.context_processors.template_settings',
            ],
        },
    },
]

# django-compressor settings
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sass --scss --quiet {infile} {outfile}'),
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    # NOTE: requires COMPRESS_ENABLED = True when DEBUG is True
    'django_compressor_autoprefixer.AutoprefixerFilter',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)


GRAPPELLI_ADMIN_TITLE = 'Derrida Admin'

WSGI_APPLICATION = 'derrida.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'sitemedia'),
]

SITE_ID = 1

# pucas configuration that is not expected to change across deploys
# and does not reference local server configurations or fields
PUCAS_LDAP = {
    # basic user profile attributes
    'ATTRIBUTES': ['givenName', 'sn', 'mail'],
    'ATTRIBUTE_MAP': {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    },
}


ANNOTATOR_ANNOTATION_MODEL = 'interventions.Intervention'

##################
# LOCAL SETTINGS #
##################

# (local settings import logic adapted from mezzanine)

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local_settings import *", we use exec so that
# local_settings has full access to everything defined in this module.
# Also force into sys.modules so it's visible to Django's autoreload.

f = os.path.join(BASE_DIR, "derrida", "local_settings.py")
if os.path.exists(f):
    import sys
    import imp
    module_name = "derrida.local_settings"
    module = imp.new_module(module_name)
    module.__file__ = f
    sys.modules[module_name] = module
    exec(open(f, "rb").read())

# if in debug mode and django-debug-toolbar is available, add to installed apps
if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    except ImportError:
        pass
