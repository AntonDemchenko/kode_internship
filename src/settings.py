import logging
import os
import sys
from datetime import timedelta
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIBPQIBAAJBAL1GZOUlgnT9UkIdCCDkOSYrtvvthtvZLJwno0gWfwODfoqS1v23
grvD8VY5ZNy+BEpZHb5a3sJILhnXq7z5Qp0CAwEAAQJBAKUSsMocpaNsj4IzmbQ9
9w2wUH11UgmJZdumwkQLwqiHVRCdCV8Y4WbM4EhCXTwcJZxAY2mY7nlwT7tbTj7c
CAECIQDho1yh7vttMNwU2clFiEjDRfS+W/w5q5EiDMwaW3QWAQIhANa+auR8dkGJ
I8izxG5KZ9q40wCyMgjoevrafwo778SdAiEAxMMufk/mlRtscApTB/2GZjLU8ENK
ugew8h5yxfFGVAECIQCRdINk5qUXOPQjExj/d6im70AFHa5keEwstGkOnpCGxQIh
AMz0OMIvk0AlJgqgkxs9g7gmdgcJ1qPqvMvWl9+jA2ac
-----END RSA PRIVATE KEY-----
"""

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL1GZOUlgnT9UkIdCCDkOSYrtvvthtvZ
LJwno0gWfwODfoqS1v23grvD8VY5ZNy+BEpZHb5a3sJILhnXq7z5Qp0CAwEAAQ==
-----END PUBLIC KEY-----
"""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', 0))

ALLOWED_HOSTS = [
    '*',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'base_app',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

ROOT_URLCONF = 'base_app.urls'

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

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#


CACHE_DEFAULT_TIMEOUT = 60

REDIS_HOST = os.environ.get('REDIS_HOST', '0.0.0.0')
REDIS_PORT = int(os.environ.get('REDIS_HOST', '6379'))
REDIS_DB = 1

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'RS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': PUBLIC_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


class MaxLevelLimit(logging.Filter):

    def __init__(self, level=logging.CRITICAL, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = level

    def filter(self, record: logging.LogRecord):
        return record.levelno <= self.level


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] (%(name)s) %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'filters': {
        'info_and_below': {
            '()': MaxLevelLimit,
            'level': logging.INFO,
        },
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filters': ['info_and_below'],
        },
        'stderr': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'level': 'WARNING',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['stderr'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
        },
    },
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_URL = '/static/'

STATIC_ROOT = '/var/static'

HOST_IP_ADDRESS = os.environ.get('HOST_IP_ADDRESS', '0.0.0.0')
