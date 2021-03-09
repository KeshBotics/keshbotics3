# Author: @Travis-Owens
# Date: 2021-02-11
# Description: This file is used for misc Discord interactions such as:
#  - Guild Owner Lookup
#  - Sending permission issue alerts to guild onwers

from classes.event_logging.event_logging import get_logger
from classes.data_handler import data_handler

import requests
import os
import json

class discord_management(object):
    def __init__(self):

        # General headers required for Discord API interactions
        self.headers = { "Authorization":"Bot {}".format(os.getenv('DISCORD_BOT_TOKEN').strip("\r")),
                         "User-Agent":"KeshBotics (v3.3)",
                         "Content-Type":"application/json"
                        }

        self.db = data_handler()


    def get_headers(self):
        # Getter function for the retrieving the headers dict
        return(self.headers)

    def get_guild_data(self, discord_guild_id = None, discord_channel_id = None):
        # Fetches the guild object, this function can perform a lookup based on either the
        # guild ID or a channel ID.
        # https://discord.com/developers/docs/resources/guild#guild-object-guild-structure

        try:
            if discord_guild_id is None and discord_channel_id is None:
                # Neither value provided
                get_logger().warning("Neither discord_guild_id nor discord_channel_id provided", exc_info=True)
                return(None)

            if discord_guild_id is None:
                # Use the find_parent_guild function to lookup the guild ID
                discord_guild_id = self.find_parent_guild(discord_channel_id)

                if discord_guild_id is None:
                    # Failed to find Guild ID
                    return(None)

            # Use the Discord API to retrieve the Guild Owners user ID
            endpoint = "https://discordapp.com/api/guilds/" + str(discord_guild_id)
            resp = requests.get(url=endpoint, headers=self.headers)

            if(resp.status_code != 200):
                # The expected response code is 200, anything else would indicate an issue
                get_logger().warning(resp.json(), exc_info=True)
                return(None)

            try:
                # Attempt to parse the response into a dict and return it
                return(resp.json())
            except:
                # Either invalid guild_id or bot lacks access to guild
                return(None)

        except Exception as e:
            # Error retrieving guild owner_id
            get_logger().error(e, exc_info=True)
            return(None)


    def find_parent_guild(self, discord_channel_id):
        # This function will return the parent guild ID of a given discord_channel_id
        # Typically, this relationship will be stored in the local database, however,
        # in the event that it is not found, a request will be made to the Discord API.
        try:
            # Search database for relationship
            # This relationship will be in either 'twitch_notifications' or 'youtube_notifications'
            # This query uses the 'UNION ALL' operator to combine the discord guild ID's from both tables.
            sql = ("SELECT `discord_guild_id` FROM `twitch_notifications` WHERE `discord_channel_id` = %s "
                    "UNION ALL SELECT `discord_guild_id` FROM `youtube_notifications` WHERE `discord_channel_id` = %s LIMIT 1"
                  )

            # Fetch the discord_guild_id
            discord_guild_id = self.db.select(sql, [discord_channel_id, discord_channel_id])

            # Determine if a discord_guild_id was found in the database
            # Expected format: [{'discord_guild_id'}].
            # If the value does not exist, the exception will trigger.
            try:
                return(discord_guild_id[0]['discord_guild_id'])
            except:
                # Discord Guild ID was not found in the databse
                discord_guild_id = None

            # Query the Discord API
            endpoint = "https://discordapp.com/api/channels/" + str(discord_channel_id)
            resp = requests.get(url=endpoint, headers=self.headers)

            if(resp.status_code != 200):
                # The expected response code is 200, anything else would indicate an issue
                get_logger().warning(resp.json(), exc_info=True)
                return(None)

            try:
                # Attempt to retreive the guild_id from the response
                return(resp.json()['guild_id'])
            except:
                # Either invalid channel ID or bot lacks access (should be caught in prior if statement)
                return(None)


        except Exception as e:
            # An exception occured while attempting to lookup the parent guild ID
            get_logger().error(e, exc_info=True)
            return(None)

    def direct_message_channel_id(self, user_id):
        # This function will return the direct message channel ID for the given user ID

        try:
            # Query the "api/users/@me/channels" endpoint

            endpoint = "https://discordapp.com/api/users/@me/channels"

            # JSON data with the recipient_id (user_id) is required
            data = json.dumps({'recipient_id':user_id})

            resp = requests.post(url=endpoint, headers=self.headers, data=data)

            if(resp.status_code != 200):
                # The expected response code is 200, anything else would indicate an issue
                get_logger().warning(resp.json(), exc_info=True)
                return(None)

            try:
                return(resp.json()['id'])
            except:
                # User ID is invalid or bot lacks permission
                return(None)


        except Exception as e:
            # Failed to retrieve direct message channel ID
            get_logger().error(e, exc_info=True)
            return(None)

    def send_direct_message(self, user_id, message):
        # Sends direct message to the given user_id

        try:
            # Get the direct message channel ID
            direct_message_channel = self.direct_message_channel_id(user_id)

            endpoint = "https://discordapp.com/api/channels/" + str(direct_message_channel) + "/messages"
            data     = json.dumps({'content':message})

            resp = requests.post(url=endpoint, headers=self.headers, data=data)

            if(resp.status_code != 200):
                # Expected status_code is 200
                get_logger().error(resp.json(), exc_info=True)
                return(False)


            return(True)
        except Exception as e:
            get_logger().error(e, exc_info=True)
            return(False)

    def alert_guild_owner_permissions(self, discord_channel_id):
        # This is used to notify a guild owner that the bot is missing the permissions
        # required to send a notification.

        try:
            # Create an event warning of the issue
            get_logger().warning(str("Missing permissions in " + str(discord_channel_id)), exc_info=True)

            # Retreive the guild data object, this contains the owner_id and guild name
            guild_data = self.get_guild_data(discord_channel_id = discord_channel_id)

            # Set the message
            message = "I've encountered an error in guild: `" + str(guild_data['name']) + "`! \n Please ensure that I'm able to read messages, send messages, and embed links in the channels you want me to operate in."

            # Send the message
            status = self.send_direct_message(guild_data['owner_id'], message)

            if status is False:
                # Failed to contact the guild owner
                # NOTE: determine if a notification should be removed
                get_logger().error("Failed to contact guild owner for channel_id: " + str(discord_channel_id), exc_info=True)

            return(status)

        except Exception as e:
            # Failed to notify the guild owner
            get_logger().error(e, exc_info=True)
            return(False)
