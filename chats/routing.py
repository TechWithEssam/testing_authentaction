from django.urls import path, re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r"^ws/dir/(?P<room_slug>\w+)/$", consumers.ChatConsumer.as_asgi()),


]
