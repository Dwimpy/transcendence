"""
Django settings for transcendence project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os.path
from pathlib import Path
from decouple import config
from django.template.context_processors import media

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&95rh562@s-za%5_ngf6a*7*@2i=ue%+3if@^lb49iq)56a0=u'



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'websocketking.com']
AUTH_USER_MODEL = 'accounts.AccountUser'


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_sass_compiler',
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
    'index',
    'accounts',
    'pong',
    'lobby',
    'widget_tweaks'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

ROOT_URLCONF = 'transcendence.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': {
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'index', 'templates'),
            os.path.join(BASE_DIR, 'api', 'templates'),
            os.path.join(BASE_DIR, 'pong', 'templates'),
            os.path.join(BASE_DIR, 'accounts', 'templates')
        },
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'index.templatetags.custom_tags',
                # 'accounts.templatetags.registration_tags'
            ],
        },
    },
]

# Logins

LOGIN_REDIRECT_URL = 'index'
ACCOUNT_LOGOUT_REDIRECT = 'index'
SITE_ID = 2  # Use the ID of the site you added in the admin
LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = 'login'

CLIENT_ID = config('FT_CLIENT_ID')
CLIENT_SECRET = config('FT_CLIENT_SECRET')
REDIRECT_URI = config('REDIRECT_URI')




# WSGI_APPLICATION = 'transcendence.wsgi.application'
ASGI_APPLICATION = 'transcendence.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': 'localhost',  # or your database host
        'PORT': '5432',  # or your database port
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# URLS
STATIC_URL = 'static/'
MEDIA_URL = 'media/'

# ROOT URLS
STATIC_ROOT = os.path.join(BASE_DIR, 'static_production_test/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'resources', 'media/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'resources', 'static/'),
    os.path.join(BASE_DIR, 'lobby', 'static/'),
    os.path.join(BASE_DIR, 'resources', 'media/')
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

SASS_PROCESSOR_OUTPUT_DIR = os.path.join(BASE_DIR, 'resources', 'static', 'css')

SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, 'resources', 'static', 'bootstrap'),
]

SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r'^.+\.scss$'
SASS_PRECISION = 8

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'