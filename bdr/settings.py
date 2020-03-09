"""
Django settings for bdr project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
from getenv import env


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', 'secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', False)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', ['localhost', '127.0.0.1'])
ASYNC_EMAILS = True
ALLOW_EDITING_COMPANIES = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #custom
    'django_q',
    'frame',
    'ckeditor',
    'simple_history',
    'memoize',
    'notifications.apps.NotificationsConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #custom
    'frame.middleware.RequestMiddleware',
    'frame.middleware.UserMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware'
]

ROOT_URLCONF = 'bdr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #custom
                'notifications.layout.layout_context_processor',
                'notifications.context.debug',
                'notifications.context.sentry',
                'notifications.context.use_sidemenu',
                'notifications.context.utils',
            ],
        },
    },
]

WSGI_APPLICATION = 'bdr.wsgi.application'

FIXTURE_DIRS = (
   'notifications/fixtures/',
)

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DATABASES_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': env('DATABASES_NAME', '/db.sqlite'),
        'USER': env('DATABASES_USER', ''),
        'PASSWORD': env('DATABASES_PASSWORD', ''),
        'HOST': env('DATABASES_HOST', ''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = env('STATIC_ROOT', os.path.join(BASE_DIR, 'static/'))

STATIC_URL = env('STATIC_URL', '/static/')

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_bdr': [
            ['Format', 'Bold', 'Italic', 'Underline', '-', 'Undo', 'Redo', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Maximize', 'ShowBlocks', '-', 'Source'],
        ],
        'toolbar': 'bdr',
        'width': '100%',
    },
}


# Authentication
# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'frame.backends.FrameUserBackend',
)

FRAME_URL = env('FRAME_URL', '')
FRAME_VERIFY_SSL = env('FRAME_VERIFY_SSL', False)
FRAME_COOKIES = env('FRAME_COOKIES', [])


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': [],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'notifications.registries': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'notifications.management': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'notifications.views': {
            'handlers': ['console'],
            'level': 'ERROR',
        }
    }
}


# BDR specific

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 3000,
        'OPTIONS' : {
            'MAX_ENTRIES': 150
        }
    }
}

APP_REVERSE_PROXY = env('APP_REVERSE_PROXY', False)

EMAIL_BACKEND = env('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', 'localhost')
EMAIL_PORT = env('EMAIL_PORT', 25)

BDR_SERVER_URL = env('BDR_SERVER_URL', 'http://localhost')
BDR_COMPANIES_PATH = env('BDR_COMPANIES_PATH', '/management/companies/export/json')
BDR_PERSONS_PATH = env('BDR_PERSONS_PATH', '/management/persons/export/json/')
BDR_EMAIL_FROM = env('BDR_EMAIL_FROM', 'bdr@localhost')

USE_ZOPE_LAYOUT = env('USE_ZOPE_LAYOUT', True)

USE_SIDEMENU = env('USE_SIDEMENU', False)
BDR_SIDEMENU_URL=env('BDR_SIDEMENU_URL', '')
BDR_API_USER = env('BDR_API_USER', '')
BDR_API_PASSWORD = env('BDR_API_PASSWORD', '')

BDRREGISTRY_URL = env('BDR_REGISTRY_URL', '')
BDRREGISTRY_USERNAME = env('BDR_REGISTRY_USERNAME', '')
BDRREGISTRY_PASSWORD = env('BDR_REGISTRY_PASSWORD', '')


ECRREGISTRY_URL = env('ECR_REGISTRY_URL', '')
ECR_COMPANY_PATH = env('ECR_COMPANY_PATH', '/undertaking/list')
ECR_PERSON_PATH = env('ECR_PERSON_PATH', '/misc/user/export/json')
ECRREGISTRY_TOKEN = env('ECR_REGISTRY_TOKEN', '')
ECR_DOMAINS = env('ECR_DOMAINS', '').split(',')
ECR_ACCEPTED_COMPANIES_STATUS=env('ECR_ACCEPTED_COMPANIES_STATUS', '').split(',')

DOUBLE_CHECK_COMPANIES = ['F-gases EU', 'F-gases NONEU', 'ODS']
EMAIL_SENDER = env('EMAIL_SENDER', '')
BCC = [env('BCC', '')]

BASE_OTRS_EMAIL_HEADERS = {
    'X-OTRS-ArticleType': 'email-internal',
    'X-OTRS-Loop': 'True',
    'X-OTRS-State': 'closed successful'
}

INVITATIONS_OTRS_EMAIL_HEADERS = {
    **BASE_OTRS_EMAIL_HEADERS,
    **{'X-OTRS-Queue': 'BDR requests::Invitations'}
}

CARSVANS_OTRS_EMAIL_HEADERS = {
    **BASE_OTRS_EMAIL_HEADERS,
    **{'X-OTRS-Queue': 'BDR requests::Cars and Vans'}
}


Q_CLUSTER = {
    'redis': {
        'host': os.environ.get('REDIS_HOST', 'redis'),
        'port': int(os.environ.get('REDIS_PORT', 6379)),
    }
}

if not DEBUG:
    INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]
    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
    }


try:
    from localsettings import *
except ImportError:
    pass


if 'test' in sys.argv:
    try:
        from localsettings_test import *
    except ImportError:
        pass
