from django.urls import re_path

import chat.consumers

websocket_urlpatterns = [
    #wysylanie
    re_path(r'ws/chat/(?P<room_id>\w+)/(?P<user_id>\w+)/$', chat.consumers.ChatConsumer.as_asgi()),
    #lista


]
