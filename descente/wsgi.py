"""
WSGI config for descente project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
import sys
import site

from django.core.wsgi import get_wsgi_application
import django.core.handlers.wsgi

path='/django/descente'

if path not in sys.path:
  sys.path.append(path)

site.addsitedir('/django/descente/ENV/py3/lib/python3.5/site-packages')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "descente.settings.eu-settings")

# application = get_wsgi_application()
application = django.core.handlers.wsgi.WSGIHandler()

# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()
