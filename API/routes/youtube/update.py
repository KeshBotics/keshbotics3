# Author: @Travis-Owens
# Date: 2021-01-18
# Desc: This is used to trigger the API to update the webhook (pubsubhubbub)
#        subcriptions and YouTube display names in the database.

import falcon
import os
import json

from classes.event_logging.event_logging import get_logger
from middleware.auth import auth
from classes.youtube.youtube_management import youtube_management

@falcon.before(auth())
class youtube_update(object):
    def __init__(self):
        pass

    def on_put(self, req, resp):

        try:
            yt_management = youtube_management()
            yt_management.update_display_names()
            yt_management.update_webhook_subs()

            resp.status = falcon.get_http_status(200)
            resp.content_type = ['application/json']
            resp.body = json.dumps({"status":"success", "code":200})

        except Exception as e:
            get_logger().error(e, exc_info=True)
            
            resp.status = falcon.get_http_status(400)
            resp.content_type = ['application/json']
            resp.body = json.dumps({"status":"error", "code":400})
