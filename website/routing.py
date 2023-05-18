from django.urls import re_path
from website import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chatroom_id>\d+)/$',
            consumers.ChatFriendConsumer.as_asgi()),
]
