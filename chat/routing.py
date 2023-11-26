from django.urls import re_path

import chat.consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', chat.consumers.ChatConsumer.as_asgi()),
]