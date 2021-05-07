# Author: @Travis-Owens
# Date: 2021-03-10
# Desc: Used to set/update, get, or delete notification limit overrides.

import falcon
import json

from middleware.auth import auth
from classes.notification_limit import notification_limit

@falcon.before(auth())
class limits(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        # Used to retrieve the overrides for a given discord_guild_id
        try:
            # The discord_guild_id is required
            discord_guild_id = req.get_header('discord-guild-id')
            if discord_guild_id is None:
                raise falcon.HTTPBadRequest('Missing Requried Headers', 'Required header(s): discord-guild-id')

            # Retrieve the limits for both Twitch and YouTube
            twitch_notification_limit = notification_limit().get_twitch_limit(discord_guild_id)
            youtube_notification_limit = notification_limit().get_youtube_limit(discord_guild_id)
            body = {"twitch": twitch_notification_limit, "youtube":youtube_notification_limit}

            resp.status = falcon.get_http_status(200)
            resp.content_type = ['application/json']
            resp.body = json.dumps(body)

        except Exception as e:
            resp.status = falcon.get_http_status(503)
            resp.content_type = ['application/json']
            resp.body = json.dumps({"status":"error", "code":503, "message":str(e)})

    def on_put(self, req, resp):
        # Used to create/update an override

        # Get header values
        discord_guild_id = req.get_header('discord-guild-id')
        platform = str(req.get_header('platform')).lower()
        override = int(req.get_header('override'))

        # Check if header values exist
        if discord_guild_id is None or platform is None or override is None:
            raise falcon.HTTPBadRequest('Missing Requried Headers', 'Required header(s): discord-guild-id, platform, override')

        # Check if platform value is valid
        if platform not in ['twitch', 'youtube']:
            raise falcon.HTTPBadRequest('Invalid Platform Header', 'Accepted platform values: twitch, youtube')

        # Set the override value for the corresponding platform
        if(platform == "twitch"):
            status = notification_limit().set_twitch_limit_override(discord_guild_id, override)
        elif(platform == "youtube"):
            status = notification_limit().set_youtube_limit_override(discord_guild_id, override)

        # Set the content type
        resp.content_type = ['application/json']

        if(status):
            # Notification limit override update was successful.
            resp.status = falcon.get_http_status(200)
            resp.body   = json.dumps({"status":"success", "code":200, "message":"Override successfully updated."})

        else:
            # Notification limit override update failed.
            resp.status = falcon.get_http_status(503)
            resp.body   = json.dumps({"status":"error", "code":503, "message":"Failed to update override."})


    def on_delete(self, req, resp):
        # Used to delete an override

        # Get header values
        discord_guild_id =  req.get_header('discord_guild_id')
        platform =  str(req.get_header('platform')).lower()

        # Check if header values exist
        if discord_guild_id is None or platform is None:
            raise falcon.HTTPBadRequest('Missing Requried Headers', 'Required header(s): discord-guild-id, platform, override')

        # Check if platform value is valid
        if platform not in ['twitch', 'youtube']:
            raise falcon.HTTPBadRequest('Invalid Platform Header', 'Accepted platform values: twitch, youtube')

        # Set the override value for the corresponding platform
        if(platform == "twitch"):
            status = notification_limit().delete_twitch_limit_override(discord_guild_id)
        elif(platform == "youtube"):
            status = notification_limit().delete_youtube_limit_override(discord_guild_id)

        # Set the content type
        resp.content_type = ['application/json']

        if(status):
            # Notification limit override update was successful.
            resp.status = falcon.get_http_status(200)
            resp.body   = json.dumps({"status":"success", "code":200, "message":"Override successfully removed."})

        else:
            # Notification limit override update failed.
            resp.status = falcon.get_http_status(503)
            resp.body   = json.dumps({"status":"error", "code":503, "message":"Failed to remove override."})
