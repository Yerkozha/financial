import os
import firebase_admin

from pathlib import Path
from datetime import timedelta

from configurations import Configuration

from firebase_admin import initialize_app, credentials, messaging

from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

print('BASE_DIR', os.path.join(BASE_DIR, 'hidjama-3326f-firebase-adminsdk-zr9nh-426699b34c.json'))
"""
    site_packages 70 line recreate raise exp
    cors
    
    event driven architecture asyncio eventemitter
    
    i18n chatGPT => model one to many language translations
    
    smtp        !!!
    sms login   !!!
     
"""
SECRET_KEY = "django-insecure-@jec7as!l!foe-6flaq7c)4*%2a#&t))oi!rq)cxt+x7k@(uke"

class BaseConfig(Configuration):


    AUTH_USER_MODEL = 'users.IndividualModel'

    SECRET_KEY = SECRET_KEY

    DEBUG = False

    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True

    INSTALLED_APPS = [
        'daphne',
        'modeltranslation',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'celery',
        'app.financial',
        'app.users',
        'app.articles',
        'rest_framework_simplejwt.token_blacklist',
        "corsheaders",
        "fcm_django",
        'channels',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        "corsheaders.middleware.CorsMiddleware",
    ]


    ROOT_URLCONF = 'config.urls'

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

    WSGI_APPLICATION = 'config.wsgi.application'

    ASGI_APPLICATION = "config.asgi.application"

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }

    # Database
    # https://docs.djangoproject.com/en/5.0/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', "django.db.backends.postgresql"),
            'NAME': os.getenv('DB_NAME', 'financial'),
            'HOST': os.getenv('DB_HOST', 'postgres'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'USER': os.getenv('DB_USER', 'financial'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
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

    LANGUAGE_CODE = 'en-us'

    LANGUAGES = (
        ("en", _("English")),
        ("kk", _("Kazakh")),
        ("ru", _("Russian")),
    )

    LOCALE_PATHS = [os.path.join(BASE_DIR, "app", "locale")]

    TIME_ZONE = 'Asia/Aqtau'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = 'http://localhost/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

    MEDIA_URL = "http://localhost/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.AllowAny',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication'
        ),
        'EXCEPTION_HANDLER': 'app.utils.exceptions.custom_exception_handler',
    }

    CELERY_BROKER_URL = "amqp://test:qwerty@rabbitmq:5672/"
    BROKER_URL = "amqp://test:qwerty@rabbitmq:5672/"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"

    CELERY_TASK_DEFAULT_QUEUE = "financial_queue"
    CELERY_IGNORE_RESULT = True

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
        'REFRESH_TOKEN_LIFETIME': timedelta(hours=1),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True,
        'ALGORITHM': 'HS256',
        'SIGNING_KEY': SECRET_KEY,
        'VERIFYING_KEY': None,
        'AUTH_HEADER_TYPES': ('Bearer',),
        'USER_ID_FIELD': 'id',
        'USER_ID_CLAIM': 'user_id',
        'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
        'TOKEN_TYPE_CLAIM': 'token_type',
    }

    FIREBASE_APP = initialize_app(credentials.Certificate(os.path.join(BASE_DIR, 'hidjama-3326f-firebase-adminsdk-zr9nh-426699b34c.json')))

    FCM_DJANGO_SETTINGS = {
        "FCM_SERVER_KEY": "AAAAa_zqcLw:APA91bG5R8WXcs0wxlQ0aaM9owrmngBgO9iqVunSuag_jJNJ1iBQ98o6YJrxTyM6e1CjNOl4dwRyCP8u4izg9HTNYb9kNVoglzNYuA0yTmTpAcEnXOCMZhCsFwyKE8Wrb4QO5hzeHktL",
    }




'''
    REST_FRAMEWORK => DEFAULT PERMISSION CLASSES CHECK TO AUTHENTICATE FCM
'''

class Dev(BaseConfig):
    DEBUG = True


class Prod(BaseConfig):
    DEBUG = False
