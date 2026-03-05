# api/routing.py

from django.urls import re_path
from .consumers import RPGConsumer


websocket_urlpatterns = [

    re_path(
        r"ws/rpg/(?P<room_id>\w+)/$",
        RPGConsumer.as_asgi()
    ),

]
