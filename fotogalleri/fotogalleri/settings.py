"""
Django settings for fotogalleri project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from getenv import env
from ldap import SCOPE_SUBTREE, OPT_X_TLS_REQUIRE_CERT, OPT_X_TLS_NEVER
from dj_database_url import parse as dj_database_parse
from django_auth_ldap.config import LDAPSearch, PosixGroupType

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', 'secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', True)

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gallery',
    'backend',
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

ROOT_URLCONF = 'fotogalleri.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'fotogalleri.wsgi.application'

# Logging
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '/var/log/fotogalleri/info.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
            'django_auth_ldap': {
                'handlers': ['file'],
                'level': 'INFO',
            },
        },
    }

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_parse(env('DATABASE', 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')))
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = 'home'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

MEDIA_URL = '/images/'
MEDIA_ROOT = env('MEDIA_ROOT', os.path.join(BASE_DIR, 'images/'))

THUMBNAILS_NAME = env('THUMBNAILS_NAME', '__thumbnails')

# REST Framework settings
# TODO: provide GET access to certain users for non-admins
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
}

# Confs necessary for ajax-select
AJAX_SELECT_INLINES = 'staticfiles'
# STATIC_ROOT = env("STATIC_ROOT", None)
STATIC_ROOT = os.path.join(BASE_DIR, 'gallery/static')

# Conf for thumbnail queue
THUMB_QUEUE_THREAD_COUNT = env('THUMB_QUEUE_THREAD_COUNT', 4)

# Enable thumbnail generation
ENABLE_THUMB_QUEUE = env('ENABLE_THUMB_QUEUE', False)

# LDAP Stuff

# Baseline configuration.
AUTH_LDAP_SERVER_URI = env("LDAP_SERVER_URI", "ldaps://localhost:45671")

AUTH_LDAP_USER_DN_TEMPLATE = env("LDAP_USER_DN_TEMPLATE", "uid=%(user)s,dc=example,dc=com")

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    env("LDAP_GROUP_DN", "ou=group,dc=example,dc=com"),
    SCOPE_SUBTREE,
    "(objectClass=posixGroup)"
)
AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr="cn")

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "uid",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

# Map LDAP group to is_staff property in Member model
# this restricts all is_staff required views to those that are members of the specified LDAP group
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_staff": env("LDAP_STAFF_GROUP_DN", "cn=superuser,ou=group,dc=example,dc=com"),
    "is_superuser": env("LDAP_SUPERUSER_GROUP_DN", "cn=superuser,ou=group,dc=example,dc=com"),
}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Mirror LDAP groups
AUTH_LDAP_MIRROR_GROUPS = True

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Never require cert
AUTH_LDAP_GLOBAL_OPTIONS = {
    OPT_X_TLS_REQUIRE_CERT: OPT_X_TLS_NEVER
}
