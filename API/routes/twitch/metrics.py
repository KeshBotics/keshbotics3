# Author: @Travis-Owens
# Date: 2020-02-28
# Description: This route is used to retreive a dictionary of recent streams

import falcon
import json

from classes.twitch_management         import twitch_handler
from classes.twitch.stream_metrics     import stream_metrics


# Stream metrics by username
class twitch_metrics_username(object):
    def __init__(self):
        pass

    def on_get(self, req, resp, twitch_username):
        twitch_handler_obj = twitch_handler()
        twitch_user_id     = twitch_handler_obj.get_twitch_user_id(twitch_username)

        data = json.dumps(stream_metrics().get_stream_metrics(twitch_user_id))

        resp.status = falcon.HTTP_200   # Set response type
        resp.content_type = ['application/json']    # Set content_type
        resp.body = data


class twitch_metrics_id(object):
    def __init__(self):
        pass

    def on_get(self, req, resp, twitch_user_id):

        data = json.dumps(stream_metrics().get_stream_metrics(twitch_user_id))

        resp.status = falcon.HTTP_200   # Set response type
        resp.content_type = ['application/json']    # Set content_type
        resp.body = data
