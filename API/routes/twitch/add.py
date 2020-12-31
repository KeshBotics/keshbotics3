# Author: @Travis-Owens
# Date:   2020-02-16
# Description: This route is used to create a notication about a defined twitch user.

import falcon
import json

from middleware.auth import auth
from classes.twitch_management import twitch_management

@falcon.before(auth())
class twitch_add(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        try:
            # Retrieve twitch_username and discrod_channel_id from headers
            twitch_username     = req.get_header('twitch-username')
            discord_channel_id  = req.get_header('discord-channel-id')

            # If twitch_username or discord_channel_id are not set then raise exception
            if(twitch_username == None or discord_channel_id == None):
                raise falcon.HTTPBadRequest('Missing Requried Headers', 'Required headers: twitch-username and discord-channel-id')

            # Using twitch_management class attempt to add new notifiaction
            message = twitch_management(twitch_username, discord_channel_id).add()

            resp.status = falcon.get_http_status(message['code'])
            resp.content_type = ['application/json']
            resp.body = json.dumps(message)


        except falcon.HTTPBadRequest as e:
            message = {"status":"error", "code":400, "message":e.description}
            resp.status = falcon.get_http_status(message['code'])
            resp.content_type = ['application/json']
            resp.body = json.dumps(message)

        except Exception as e:
            print(str(e))
            resp.body = "API ERROR"
