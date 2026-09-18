"""
WSGI config for skillsetu_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsetu_backend.settings')

application = get_wsgi_application()

# Start background database keep-alive daemon for serverless Neon Postgres
try:
    from skillsetu_backend.db_keepalive import start_db_keepalive
    start_db_keepalive()
except Exception:
    pass

