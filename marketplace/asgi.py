from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import os
from django.core.asgi import get_asgi_application



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')

django_asgi_app = get_asgi_application()
import chats.routing
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chats.routing.websocket_urlpatterns))
        ),
    }
)