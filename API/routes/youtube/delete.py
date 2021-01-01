# Author: @Travis-Owens
# Date: 2020-10-17
# Description: This class is used to delete YouTube notifiaction to the database.

# Related Routes:
# - /youtube/manage/delete

import falcon
import json

from middleware.auth import auth
from classes.youtube.youtube_management import youtube_management

@falcon.before(auth())
class youtube_delete(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        try:
            # Retrieve the Discord channel ID and the YouTube channel URL from the headers
            disc_channel_id  = req.get_header('discord-channel-id')
            yt_channel_url   = req.get_header('youtube-channel-url')

            # If either of the two required headers are missing, return bad request
            if(disc_channel_id == None or yt_channel_url == None):
                raise falcon.HTTPBadRequest('Missing Requried Headers', 'Required headers: discord-channel-id and youtube-channel-url')

            # Using the youtube_management class add the subscription to the database
            message = youtube_management().unsubscribe(yt_channel_url, disc_channel_id)

            resp.status = falcon.get_http_status(message['code'])
            resp.content_type = ['application/json']
            resp.body = json.dumps(message)

        except falcon.HTTPBadRequest as e:
            message = {"status":"error", "code":400, "message":e.description}
            resp.status = falcon.get_http_status(message['code'])
            resp.content_type = ['application/json']
            resp.body = json.dumps(message)
