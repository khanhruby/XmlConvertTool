from .base import *

SECRET_KEY = '*u1(#u5t_9hw(6)l@+7cyvgpqyzw_^g+0!ymn7ss!nn_+$qf5w'
DEBUG = True

TEMPLATE_DEBUG = True
CSRF_COOKIE_NAME = 'localhost_csrf_jp'
CSRF_COOKIE_DOMAIN = 'jp.app'

# import uwsgi
# from uwsgidecorators import timer
# from django.utils import autoreload

# @timer(3)
# def change_code_gracefull_reload(sig):
#     if autoreload.code_changed():
#         uwsgi.reload()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*u1(#u5t_9hw(6)l@+7cyvgpqyzw_^g+0!ymn7ss!nn_+$qf5w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '1.2.3.4', 'demandware-tool.com', 'jp.app', 'eu.app', '172.16.20.4', '172.16.20.50']
CSRF_COOKIE_NAME = 'localhost_csrf_jp'
CSRF_COOKIE_DOMAIN = 'jp.app'
WSGI_APPLICATION = 'descente.wsgi.application'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'dsnt_tool',
    #     'USER': 'django',
    #     'PASSWORD': 'secret',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    #     'CHARSET': 'utf8',
    #     'COLLATION': 'utf8_general_ci',
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dsnt_eu',
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
