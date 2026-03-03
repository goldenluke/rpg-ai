"""
ASGI config for core project.

Configuração para:
- HTTP (Django normal)
- WebSocket (Django Channels)
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import api.routing  # Importa as rotas WebSocket

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Aplicação HTTP tradicional
django_asgi_app = get_asgi_application()

# Aplicação principal ASGI
application = ProtocolTypeRouter({

    # Requisições HTTP normais
    "http": django_asgi_app,

    # WebSockets
    "websocket": AuthMiddlewareStack(
        URLRouter(
            api.routing.websocket_urlpatterns
        )
    ),

})
