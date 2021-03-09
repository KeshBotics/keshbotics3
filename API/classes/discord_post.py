# Author: Travis-Owens
# Date: 2020-02-20
# Description: General purpose class for sending messages to Discord channels.

import json
import requests
import os
import random
import string

from classes.event_logging.event_logging import get_logger
from classes.notifications import notifications
from classes.discord.discord_management import discord_management

class discord_post(object):
    def __init__(self):
        self.headers = { "Authorization":"Bot {}".format(os.getenv('DISCORD_BOT_TOKEN').strip("\r")),
                        "User-Agent":"KeshBotics (v3.3)",
                        "Content-Type":"application/json", }

    def post_message(self, message, discord_channel_ids):
        # Used to send a message to an array of discord channel IDs
        # This is called for both Twitch and YouTube notifications

        # Convert the message dict into a JSON object
        json_data = json.dumps(message)

        for channel_id in discord_channel_ids:
            try:
                discord_message_url = "https://discordapp.com/api/channels/{}/messages".format(channel_id)
                r = requests.post(discord_message_url, headers = self.headers, data = json_data)

                if(r.status_code == 404 and r.json()['message'] == "Unknown Channel"):
                    # Discord channel no longer exist, delete notifications associated
                    # with the discord_channel_id
                    notifications().delete_by_discord_channel_id(channel_id)

                if(r.status_code == 403 and r.json()['message'] == "Missing Permissions"):
                    # The bot is missing permissions for the discord channel ID
                    discord_management().alert_guild_owner_permissions(channel_id)

            except Exception as e:
                get_logger().error(e, exc_info=True)

    def prepare_twitch_message(self, twitch_username, twitch_thumbnail_url):
        twitch_channel_url = 'https://twitch.tv/' + twitch_username
        twitch_channel_preview_url = twitch_thumbnail_url.format(width=640,height=360)
        twitch_channel_preview_url += "?uid=" + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])  #This prevents discord from caching the thumbnail and serving old thumbnails


        message = {
              "content": str(twitch_username + " is live on Twitch! " + twitch_channel_url),
              "embed": {
                "title": twitch_channel_url,
                "description": "",
                "url": twitch_channel_url,
                "color": 9442302,
                "timestamp": "",
                "footer": {
                  "icon_url": twitch_channel_preview_url,
                  "text": "KeshBotics"
                },
                "thumbnail": {
                  "url": "https://cdn.discordapp.com/avatars/532575955324239882/653f3b3749c3da11947a70881d675160.png?size=256"
                },
                "image": {
                  "url": twitch_channel_preview_url
                },
                "author": {
                  "name": "KeshBotics",
                  "url": "https://discordapp.com",
                  "icon_url": "https://cdn.discordapp.com/avatars/532575955324239882/653f3b3749c3da11947a70881d675160.png?size=256"
                },
                "fields": [
                          {
                            "name": "Twitch",
                            "value": str(twitch_username + " is live on Twitch!")
                          }
                        ]
              }
            }

        return(message)
