import os
import configparser

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^ma$9!rq*=6)*6br$eaw6dg564id*^86r93x)@x23#4g5+_181'

# Allowing access to the web service from any domain
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# Config
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'settings.ini'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(config.get('SETTINGS', 'DEVELOPMENT'))

VERSION = 'DEVELOPMENT' if DEBUG else 'PRODUCTION'
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REST Framework
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Project apps
    'apps.timetable.apps.TimetableConfig',
    'apps.telegram.apps.TelegramConfig',
    'apps.core.apps.CoreConfig',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.get(VERSION, 'NAME'),
        'HOST': config.get(VERSION, 'HOST'),
        'PORT': config.get(VERSION, 'PORT'),
        'USER': config.get(VERSION, 'USER'),
        'PASSWORD': config.get(VERSION, 'PASSWORD')
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication'],
    'TEST_REQUEST_DEFAULT_FORMAT': 'multipart'
}

# Authentication model
# AUTH_USER_MODEL =  'accounts.User'

# STATIC_ROOT
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# TELEGRAM
TELEGRAM_ADMIN_CHAT = config['TELEGRAM']['ADMIN_CHAT']
TELEGRAM_PARSER_CHAT = config['TELEGRAM']['PARSER_CHAT']
TELEGRAM_API_TOKEN = config['TOKENS']['TELEGRAM']
