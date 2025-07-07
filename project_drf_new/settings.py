import os

from pathlib import Path

from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = []

# Application definition


INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    'users',

    'lms',

    # DRF

    'rest_framework',

    'django_filters',

    'rest_framework_simplejwt',

]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'project_drf_new.urls'

TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],

        },

    },

]

WSGI_APPLICATION = 'project_drf_new.wsgi.application'

# Database

# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# НАСТРОЙКИ ДЛЯ PostgreSQL - теперь берем из .env

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}


# Password validation

# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators


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

# https://docs.djangoproject.com/en/5.2/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = 'static/'

# Default primary key field type

# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL-адрес для доступа к медиа-файлам

MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

}

# Настройка JWT токенов


SIMPLE_JWT = {

    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),

    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    "ROTATE_REFRESH_TOKENS": False,

    "BLACKLIST_AFTER_ROTATION": False,

    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",

    "SIGNING_KEY": SECRET_KEY,  # Используем SECRET_KEY из .env

    "VERIFYING_KEY": "",

    "AUDIENCE": None,

    "ISSUER": None,

    "JWK_URL": None,

    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),

    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    "USER_ID_FIELD": "id",

    "USER_ID_CLAIM": "user_id",

    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),

    "TOKEN_TYPE_CLAIM": "token_type",

    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),

    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

}

# Celery settings - могут быть в .env, но пока оставим здесь для примера

# URL для подключения к брокеру сообщений Redis

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

# URL для хранения результатов выполнения задач

CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Формат сериализации/десериализации данных для задач

CELERY_TASK_SERIALIZER = 'json'

# Формат сериализации/десериализации результатов

CELERY_RESULT_SERIALIZER = 'json'

# Принимаемые форматы содержимого

CELERY_ACCEPT_CONTENT = ['json']

# Часовой пояс

CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE', 'Europe/Moscow')

# Можно отключить ограничение скорости задач по умолчанию, если не нужно

CELERY_TASK_ACKS = True

# Email settings - теперь берем из .env

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER