# admin credentials
# hemant - hemant
import logging
import os
from datetime import timedelta
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from celery.schedules import crontab

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename='lotus_petal.log',filemode='a',format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
                    )
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a-k7fh77a=v2uc^6i_p5l=57yy8()nhx9#7#(tq752a6z5r4l_'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

'''NOTE : debug comment while go to production'''
DEBUG = int(os.environ.get("DEBUG", default=1))

ALLOWED_HOSTS = [
    'localhost',
    'studywell.lotuspetalfoundation.org',
    '35.154.251.221',
    # 'studywell.lotuspetalfoundation.org',
    'test-studywell.lotuspetalfoundation.org',
    '65.2.82.254',
    '65.0.18.223',
    '15.206.124.251',
    '13.126.5.217',
    '0.0.0.0',
    '*'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # Add this

    # Add the following django-allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # for Google OAuth 2.0


    'android_app.apps.AndroidAppConfig',
    'attendance.apps.AttendanceConfig',
    'dashboard.apps.DashboardConfig',
    'timetable.apps.TimetableConfig',
    'user_api',

    'substitution',

    'rest_framework',
    'corsheaders',

    'django_celery_results',
    'django_extensions',

    'import_export',
    'rangefilter',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # new must be placed above CommonMiddleware
    # 'django.middleware.common.CommonMiddleware',  # new

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = '_lotus_petal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'reactjs'),os.path.join(BASE_DIR, 'UI/templates')],

        # 'DIRS': ["UI/templates"],
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
WSGI_APPLICATION = '_lotus_petal.wsgi.application'


#Database
#https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'lotus_petal_user',
#         'PASSWORD': 'lotus_petal_password',
#         'HOST': 'postgres',
#         'PORT': '5432',
#
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'yourdatabasename.db'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CELERY_BROKER_URL = 'pyamqp://rabbitmq:rabbitmq@rabbitmq//'

CELERY_TIMEZONE = 'Asia/Kolkata'

# CELERY_RESULT_BACKEND = 'django-db'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
# CELERY_IMPORTS = ['dashboard.tasks']

# CELERY_BEAT_SCHEDULE = {
#     'test': {
#         'task': 'dashboard.tasks.test',
#         'schedule': crontab(minute='*/1')
#     }
# }


# sentry config
sentry_sdk.init(
    dsn="https://c871b3fc6c4e4b85b4658189fc28da09@o1029629.ingest.sentry.io/5996642",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)





LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s %(levelname)s from *** %(name)s ***  => %(message)s')},
        'simple': {
            'format': '%(levelname)s %(message)s'}},

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        # 'require_debug_false': {
        #     '()': 'django.utils.log.RequireDebugFalse'},

        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
                        },
        },
        'loggers': {
            'django': {
                'handlers': ['sentry'],
                'level': 'DEBUG',
                'propagate': True},
            # 'django.server': {
            #     'handlers': ['console'],
            #     'level': 'INFO',
            #     'propagate': True},
            # 'werkzeug': {
            #     'handlers': ['console'],
            #     'level': 'DEBUG',
            #     'propagate': True},
            # 'cch_icd.applications': {
            #     'handlers': ['console'],
            #     'level': 'DEBUG',
            #     'propagate': True}
        }
    }
}
# =================================================================================================




# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# CORS_ORIGIN_WHITELIST = [
#         'http://localhost:3000'
# ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "_lotus_petal/static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "reactjs", "build", "static" ),
    os.path.join(BASE_DIR, "reactjs", "build-timetable", "static" ),
    os.path.join(BASE_DIR, "reactjs", "build-attendance", "static" ),
)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")



# New config for JWT ( json web token )
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ]
# }



# config for Token Expiry Duration-
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15), #token will be expire in 2 hours
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30), #automatically refresh in 2 days
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY':SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


APPEND_SLASH=False #use for '/' is required in closing url


'''NOTE   config for email sen on sentry exceptions'''
ADMINS = [('nadeemali2502@gmail.com') , ('nadeem.ali@stackfusion.io'), ('sumeet@stackfusion.io'),('ravinder.kumar@stackfusion.io')]



# Email setting
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'apps@lotuspetalfoundation.org'
EMAIL_HOST_PASSWORD = 'lotus@2019'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'




# Config for Corse-Headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
                            'https://test-studywell.lotuspetalfoundation.org',
                            'https://studywell.lotuspetalfoundation.org',
                            'http://13.232.241.142:3001',
                            'http://13.126.5.217:3001'
                        ]

# Update user model
AUTH_USER_MODEL = 'user_api.User'







# google auth code
SITE_ID = 1
LOGIN_REDIRECT_URL = "/dashboard"

# Additional configuration settings
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET= True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]