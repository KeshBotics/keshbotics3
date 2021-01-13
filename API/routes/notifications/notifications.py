# Author: @Travis-Owens
# Date: 2021-01-12
# Desc: Used to retreive a list of notifications by discord_channel_id

import falcon
import json

from middleware.auth import auth
from classes.notifications import notifications

@falcon.before(auth())
class get_notificaitons(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):

        try:
            # Check if discord-channel-id is in headers, if not return HTTPBadRequest
            discord_channel_id =  req.get_header('discord-channel-id')
            if discord_channel_id is None:
                raise falcon.HTTPBadRequest('Missing Requried Headers', 'Required header(s): discord-channel-id')

            # Create object for notificaions class, get notification data for twitch and youtube
            # If no notifications are found, type None will be returned
            notifications_obj = notifications()
            twitch_notifications  = notifications_obj.get_twitch_notifications(discord_channel_id)
            youtube_notifications = notifications_obj.get_youtube_notifications(discord_channel_id)

            # Create dict with notification data
            data = { discord_channel_id: {
                        'twitch':twitch_notifications,
                        'youtube':youtube_notifications
                        }
                   }

            # Set http status to 200, set content_type to JSON, and convert the data dict into JSON
            resp.status = falcon.get_http_status(200)
            resp.content_type = ['application/json']
            resp.body = json.dumps(data)

        except falcon.HTTPBadRequest as e:
            message = {"status":"error", "code":400, "message":e.description}
            resp.status = falcon.get_http_status(message['code'])
            resp.content_type = ['application/json']
            resp.body = json.dumps(message)

        except Exception as e:
            message = {"status":"error", "code":400, "message":'API ERROR'}
            resp.status = falcon.get_http_status(message['code'])
            resp.content_type = ['application/json']
            resp.body = json.dumps(message)
