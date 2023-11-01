"""
Django settings for project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

from env_settings import EnvSettings

ENV = EnvSettings()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = ENV.DJ.SECRET_KEY

DEBUG = ENV.DJ.DEBUG

ALLOWED_HOSTS = ENV.DJ.ALLOWED_HOSTS

CSRF_TRUSTED_ORIGINS = ENV.DJ.CSRF_TRUSTED_ORIGINS

# Application definition

INSTALLED_APPS = [
    # third party patches
    'django_non_dark_admin',

    # `django.forms` app installation is required to enable switching of settings.FORM_RENDERER to
    # non default TemplatesSetting renderer.
    # https://docs.djangoproject.com/en/4.2/ref/forms/renderers/#templatessetting
    'django.forms',

    # contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'debug_toolbar',
    'django_json_widget',

    # custom apps
    'auth.apps.AuthConfig',
    'tg_bot.apps.TgBotConfig',
    'trigger_funnel.apps.AppConfig',

    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',  # should be close to the list bottom
]

ROOT_URLCONF = 'project.urls'

_TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
if ENV.TEMPLATES_ARE_CACHED:
    _TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader', _TEMPLATE_LOADERS),
    ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': _TEMPLATE_LOADERS,
        },
    },
]
# Use non default form renderer to fix aggressive template caching. It slows down the development
# of widget templates dramatically.
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ENV.POSTGRES_DSN.path.lstrip('/'),
        'USER': ENV.POSTGRES_DSN.user,
        'PASSWORD': ENV.POSTGRES_DSN.password,
        'HOST': ENV.POSTGRES_DSN.host,
        'PORT': ENV.POSTGRES_DSN.port,
        'ATOMIC_REQUESTS': True,
    },
}

# Кастомная модель пользователя
AUTH_USER_MODEL = 'project_auth.User'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Yandex object storage

if ENV.S3_DSN:
    AWS_S3_ENDPOINT_URL = ENV.s3_credentials.endpoint_url
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'project.storage_backends.MediaStorage'

    AWS_ACCESS_KEY_ID = ENV.s3_credentials.access_key_id
    AWS_SECRET_ACCESS_KEY = ENV.s3_credentials.secret_access_key
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_STORAGE_BUCKET_NAME = ENV.s3_credentials.bucket_name
    AWS_LOCATION = 'static'
    STATIC_URL = f'{AWS_LOCATION}/'
else:
    STATIC_URL = ENV.DJ.STATIC_URL
    STATIC_ROOT = '/collected_static'

    MEDIA_URL = ENV.DJ.MEDIA_URL
    MEDIA_ROOT = '/media'

STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: ENV.ENABLE_DEBUG_TOOLBAR,
}

DISABLE_DARK_MODE = True

if ENV.ROLLBAR:
    ROLLBAR = {
        'access_token': ENV.ROLLBAR.BACKEND_TOKEN,
        'environment': ENV.ROLLBAR.ENVIRONMENT,
        'root': BASE_DIR,
        'locals': {
            'safe_repr': False,  # enable repr(obj)
        },
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'tg_bot': {
            'handlers': ['console'],
            'level': ENV.TG_BOT_LOGGING_LEVEL,
        },
        'django_tg_bot_framework': {
            'handlers': ['console'],
            'level': ENV.DJANGO_TG_BOT_FRAMEWORK_LOGGING_LEVEL,
        },
        'trigger_funnel.mailing': {
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}
