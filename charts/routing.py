from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/fetch/(?P<ytid>[0-9A-Za-z_-]{11})/$', consumers.FetchConsumer.as_asgi(), name="fetch_consumer"),
]
