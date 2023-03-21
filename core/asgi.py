"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import tic_tac_toe.routings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": 
        AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(tic_tac_toe.routings.websocket_urlpatterns)
        ))
})
