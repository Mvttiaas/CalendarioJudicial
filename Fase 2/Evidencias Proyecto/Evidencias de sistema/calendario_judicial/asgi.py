"""
ASGI config for calendario_judicial project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calendario_judicial.settings')

application = get_asgi_application()
