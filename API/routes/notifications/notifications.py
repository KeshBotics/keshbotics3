# Author: @Travis-Owens
# Date: 2021-01-12
# Desc: Used to retreive a list of notifications by discord_channel_id

import falcon
import json

from classes.event_logging.event_logging import get_logger
from middleware.auth import auth
from classes.notifications import notifications
from classes.discord.discord_management import discord_management
from classes.notification_limit import notification_limit

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

            # Get the parent guild of the discord_channel_id
            discord_guild_id = discord_management().find_parent_guild(discord_channel_id)

            # Create object for notifications class, get notification data for twitch and youtube
            # If no notifications are found, type None will be returned
            notifications_obj = notifications()

            # Create object for notification limit class, get notification limit and number of
            # notifications registered for each platform
            notification_limit_obj = notification_limit()

            # Create dict with notification data
            data = { discord_channel_id: {
                        'twitch':notifications_obj.get_twitch_notifications(discord_channel_id),
                        'youtube':notifications_obj.get_youtube_notifications(discord_channel_id),
                        'limits': {
                            'twitch': {
                                'limit': notification_limit_obj.get_twitch_limit(discord_guild_id),
                                'used': notification_limit_obj.get_twitch_notification_count(discord_guild_id)
                                },
                            'youtube': {
                                'limit': notification_limit_obj.get_youtube_limit(discord_guild_id),
                                'used': notification_limit_obj.get_youtube_notification_count(discord_guild_id)
                                }
                            }
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
            get_logger().error(e, exc_info=True)

            message = {"status":"error", "code":400, "message":'API ERROR'}
            resp.status = falcon.get_http_status(message['code'])
            resp.content_type = ['application/json']
            resp.body = json.dumps(message)

    def on_delete(self, req, resp):
        # Used to delete notifications associated with either a discord_channel_id
        # or a discord_guild_id
        try:
            # Check if discord-channel-id or discord-guild-id is in the headers, else HTTPBadRequest
            if req.get_header('discord-channel-id') is not None:
                notifications().delete_by_discord_channel_id(req.get_header('discord-channel-id'))

            elif req.get_header('discord-guild-id') is not None:
                notifications().delete_by_discord_guild_id(req.get_header('discord-guild-id'))

            else:
                raise falcon.HTTPBadRequest('Missing Requried Headers', 'Required header(s): discord-channel-id or discord-guild-id')

            resp.status = falcon.get_http_status(200)
            resp.content_type = ['application/json']
            resp.body = json.dumps({"status":"success", "code":200})

        except falcon.HTTPBadRequest as e:
            message = {"status":"error", "code":400, "message":e.description}
            resp.status = falcon.get_http_status(message['code'])
            resp.content_type = ['application/json']
            resp.body = json.dumps(message)

        except Exception as e:
            get_logger().error(e, exc_info=True)

            message = {"status":"error", "code":400, "message":'API ERROR'}
            resp.status = falcon.get_http_status(message['code'])
            resp.content_type = ['application/json']
            resp.body = json.dumps(message)
