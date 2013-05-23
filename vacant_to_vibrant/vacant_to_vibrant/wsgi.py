"""
WSGI config for vacant_to_vibrant project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacant_to_vibrant.settings")

activate_this = os.path.expanduser("~/.virtualenvs/v2v/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

project = os.path.expanduser('~/webapps/django_gu/v2v/vacant_to_vibrant')
workspace = os.path.dirname(project)
sys.path.append(workspace)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
