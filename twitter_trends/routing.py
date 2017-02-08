from . import consumers
from django.conf.urls import include


channel_routing = {
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}
# stream_channel_routing = {
#     'websocket.connect': consumers.ws_tweet_connect,
#     'websocket.receive': consumers.ws_tweet_receive,
#     'websocket.disconnect': consumers.ws_tweet_disconnect,
# }

routing = [
    # You can use a string import path as the first argument as well.
    include(channel_routing, r"^/twitter_trends/trends/"),
]