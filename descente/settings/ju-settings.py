from .base import *

SECRET_KEY = 'ju447rvbg@obims+vb7bx-4xd_pmgmu0ck35!tare5!ufqprtnukdescente'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

CSRF_COOKIE_NAME = 'localhost_csrf_ju'
CSRF_COOKIE_DOMAIN = None

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dsnt_ju',
        'USER': 'django',
        'PASSWORD': 'secret',
        'HOST': 'localhost',
        'PORT': '3306',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
    },
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


MULTIPLE_LANGUAGE = False
LANGEUAGE_MAPPING = {
    'en':'en-GB',
    'fr':'fr-FR',
    'it':'it-IT',
    'ru':'ru-RU',
    'es':'es-ES',
}
