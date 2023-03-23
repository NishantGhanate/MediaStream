"""
Django settings for media_stream project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

ALLOWED_HOSTS = ['*']

GOOGLE_FORM_URL = config('GOOGLE_FORM_URL')

WHATS_APP_LINK = config('WHATS_APP_LINK')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'corsheaders',
    'captcha',
    'video_app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

    
ROOT_URLCONF = 'media_stream.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'video_app.context_processors.get_google_form',
                'video_app.context_processors.get_whatsapp_link',
            ],
        },
    },
]

WSGI_APPLICATION = 'media_stream.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'CONN_MAX_AGE': 500,
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'NAME': config('POSTGRES_DB'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config('TIME_ZONE')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'video_app'),
# )

# Media storage path 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') # 'media' is my media folder
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'video_app.CustomUser'

# # CELERY SETTING
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_TIMEZONE = config('TIME_ZONE')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
CELERY_CACHE_BACKEND = 'default'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHE_TTL = 60 * 15

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('CACHE_LOCATION'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "MEDIA_STREAM"
    }
}

# REST configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'EXCEPTION_HANDLER': 'media_stream.utils.exception_handler.custom_exception_handler',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM': 'version',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS' : 'media_stream.utils.custom_pagination.CustomPagination'
}

# App logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'add_ip_address': {
            '()': 'media_stream.utils.custom_logfilter.IPAddressFilter' 
        }
    },
    'formatters': {
        # 'django.server': {
        #     '()': 'django.utils.log.ServerFormatter',
        #     'format': '[{server_time}] {message}',
        #     'style': '{',
        # },
        'ip_request': {
            'format': (u'%(asctime)s [%(levelname)-5s] - %(ip)s  %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'process' :{
            'format': (u'%(asctime)s [%(levelname)-5s] (%(module)s.%(funcName)s) %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'console': {
            'format': (u'%(asctime)s [%(levelname)-5s] (%(module)s.%(funcName)s) %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        # 'django.server': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': './logs/django.log',
        #     'formatter': 'ip_request',
        #     'maxBytes': 1024*1024*5,
        #     "backupCount": 3
        # },
        'video_app.file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/video_app.log',
            'formatter': 'process',
            'maxBytes': 1024*1024*5,
            "backupCount": 3
        },
        'video_convert.file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/video_convert.log',
            'formatter': 'process',
            'maxBytes': 1024*1024*5,
            "backupCount": 3
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        # 'django.server': {
        #     'handlers': ['console','django.server'],
        #     'level': 'INFO',
        #     'propagate': False,
        #     'filters': ['add_ip_address']
        # },
        'video_app': {
            'handlers': ['console', 'video_app.file'],
            'level': 'INFO',
            'propagate': True,
        },
        'video_convert': {
            'handlers': ['console', 'video_convert.file'],
            'level': 'INFO',
            'propagate': True
        },
    },
}
