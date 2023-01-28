import os
from datetime import timedelta
from pathlib import Path

# путь к папке проекта

BASE_DIR = Path(__file__).resolve().parent.parent


# ключ безопасности. используется ядром джанго и подсист.разграничения доступа

SECRET_KEY = 'django-insecure-tu$&!j*=-ha2%6@l8_pv-9fkcxd@hm%b_hyoo98p4b03*he)&e'

# дебаг режим

DEBUG = True

ALLOWED_HOSTS = []


# список зарегистрированных приложений
# admin - админский сайт джанго
# auth - встроенная система разграничения доступа, использ.админкой
# contenttypes - хранит список всех моделей. исп-ся для полиморфных связей.
# sessions - обрабатывает серверные сессии. исп-ся админкой
# messages - выводит всплывающие сообщения. исп-ся админкой
# staticfiles - обрабатывает статику

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'recipes',
    'users',
    'api',
    'djoser',

]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
APPEND_SLASH=False

SIMPLE_JWT = {
    # Устанавливаем срок жизни токена
   'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
   'AUTH_HEADER_TYPES': ('Bearer',),
}
# Посредник, обрабатывает запрос перед отправкой во view
# SecurityMiddleware - доп. защита от сетевых атак
# SessionMiddleware - обрабатывает серверные сессии
# CommonMiddleware - участрует в предварительной обработке запроса (?)
# CsrfViewMiddleware - защита от межсайтовых атак
# AuthenticationMiddleware - добавляет атрибут, хранящий текущего пользователя
# MessageMiddleware - обрабатывает высплывающие сообщения
# XFrameOptionsMiddleware - доп. зашита от сетевых атак

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# путь к маршрутам на уровне проекта
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


# настройка БД

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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
# язык для сплывающих сообщений и админки

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

# будут ли системные сообщения автоматом переводиться на язык из LANGUAGE_CODE

USE_I18N = True

# будет ли джанго хранить значения даты и времени с отметкой о TIME_ZONE

USE_TZ = True


# путь до статики

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = ('static',)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
