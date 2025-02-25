"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import sys
from pathlib import Path
from .localsetting import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# APPS_FATHER_DIR = Path(__file__).resolve().parent.parent
# sys.path.insert(0,os.path.join(APPS_FATHER_DIR, "apps"))
# sys.path.insert(0,os.path.join(APPS_FATHER_DIR, "middleware"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    'captcha',
    'apps.user',
    'apps.quiz'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.handler_middleware.Middleware'
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
SHELL_PLUS_PRE_IMPORTS = []
apps_path = os.path.join(BASE_DIR, "apps")
all_apps_fold = os.listdir(apps_path)
for model_file in all_apps_fold:
    # if os.path.isfile(os.path.join(model_path, model_file)):
        SHELL_PLUS_PRE_IMPORTS.append(
            "from {} import *".format('apps.' + model_file+'.models')
        )


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# USE_TZ = True
TIME_ZONE = 'Asia/Shanghai' 

USE_I18N = True


try:
    CORS_ALLOWED_ORIGINS.append('http://localhost:3000')
except Exception as e:
    CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
      

TOKEN_AGE = 10

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'user.User'

AUTHENTICATION_SKIP_URL = {
     '/api/user/register': ['POST'],
     '/api/user/login': ['POST'],
     '/api/docs': ['GET'],
     '/api/openapi.json': ['GET'],
     '/api/user/get_captcha': ['GET'],
     '/captcha.image/': ['GET'],
     '/api/user/validate_captcha': ['POST'],
     '/api/user/valid_email_code': ['POST'],
     '/api/user/send_email_code': ['POST']
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",  # Redis服务器地址和数据库编号
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "drq12345."
        },
        "KEY_PREFIX": "myapp",  # 可选：为所有缓存键添加前缀
    }
}
