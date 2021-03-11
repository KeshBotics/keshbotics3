# Author: @Travis-Owens
# Date: 2021-03-09
# Description: This class is used to apply a limit on the number of notifications
#               that each guild can have.

import os

from classes.event_logging.event_logging import get_logger
from classes.data_handler import data_handler

class notification_limit(object):
    def __init__(self):
        self.db = data_handler()

    # GET functions for notification limits
    def get_twitch_limit(self, discord_guild_id):
        # Helper function for the 'get_override_value' function
        # This will return the Twitch notification limit for the given discord_guild_id.

        override = self.get_override_value('twitch', discord_guild_id)

        if override is None:
            # An override for the given discord_guild_id is not found
            return(int(os.getenv('TWITCH_NOTIFICATION_LIMIT')))

        return(override)

    def get_youtube_limit(self, discord_guild_id):
        # Helper function for the 'get_override_value' function
        # This will return the YouTube notification limit for the given discord_guild_id.
        override = self.get_override_value('youtube', discord_guild_id)

        if override is None:
            # An override for the given discord_guild_id is not found
            return(int(os.getenv('TWITCH_NOTIFICATION_LIMIT')))

        return(override)

    def get_override_value(self, platform, discord_guild_id):
        # This function will select the proper SQL statement based on the given
        #  platform value, expected platform values: ['twitch', 'youtube']
        # Returns override value if exist else returns None.

        try:
            platform = str(platform).lower()

            sql = "SELECT `override` FROM `notification_limit_overrides` WHERE `platform` = %s AND `discord_guild_id` = %s"

            res = self.db.select(sql, [platform, discord_guild_id])

            return(int(res[0]['override']))

        except (TypeError, IndexError) as e:
            # Expected exception if the override value does not exist
            return(None)

        except Exception as e:
            # Unexpected exception, log event
            get_logger().error(e, exc_info=True)
            return(None)

    # SET functions for notification limits
    def set_twitch_limit_override(self, discord_guild_id, override):
        # Helper function for set_limit_override
        # This function is used to set/update twitch notification overrides.
        return(self.set_limit_override('twitch', discord_guild_id, override))

    def set_youtube_limit_override(self, discord_guild_id, override):
        # Helper function for set_limit_override
        # This function is used to set/update youtube notification overrides.
        return(self.set_limit_override('youtube', discord_guild_id, override))

    def set_limit_override(self, platform, discord_guild_id, override):
        # This function will either create an override or update an existing override

        # Determine if override exist for the given platform and discord_guild_id combination
        if self.get_override_value(platform, discord_guild_id) is None:
            # Insert override as one does not exist
            sql = "INSERT INTO `notification_limit_overrides` VALUES (NULL, %s, %s, %s)"
            res = self.db.insert(sql, [platform, discord_guild_id, override])

        else:
            # Update override as one does exist
            sql = "UPDATE `notification_limit_overrides` SET `override` = %s WHERE `platform` = %s AND `discord_guild_id` = %s"
            res = self.db.insert(sql, [override, platform, discord_guild_id])

        # Res is a bool indicating if the query was successful
        return(res)

    # DELETE functions for notification limits
    def delete_twitch_limit_override(self, discord_guild_id):
        # Helper function for delete_limit_override
        return(self.delete_limit_override('twitch', discord_guild_id))

    def delete_youtube_limit_override(self, discord_guild_id):
        # Helper function for delete_limit_override
        return(self.delete_limit_override('youtube', discord_guild_id))

    def delete_limit_override(self, platform, discord_guild_id):
        # This function will delete an override from the database

        sql = "DELETE FROM `notification_limit_overrides` WHERE `platform` = %s AND `discord_guild_id` = %s"
        res = self.db.delete(sql, [platform, discord_guild_id])

        # Res is a bool indicating if the query was successful
        return(res)

    # Functions for checking if notification limit is reached/exceeded
    def twitch_limit_reached(self, discord_guild_id):
        # Returns True if the limit on Twitch notifications is reached for
        #  the given discord_guild_id.
        # Retrurns False if the limit is not reached.

        # Create an SQL query to count the number of Twitch notifications
        sql = "SELECT count(`id`) as 'count' FROM `twitch_notifications` WHERE `discord_guild_id` = %s"
        res = self.db.select(sql, [discord_guild_id])

        # Check if the 'count' is equal to or greater than the Twitch notification limit
        if(res[0]['count'] >= self.get_twitch_limit(discord_guild_id)):
            # The limit has been reached or exceeded, return True
            return(True)

        # The limit has not been reached
        return(False)

    def youtube_limit_reached(self, discord_guild_id=None, discord_channel_id=None):
        # Returns True if the limit on YouTube notifications is reached for
        #  the given discord_guild_id.
        # Returns False if the limit is not reached.

        # Create an SQL statement to count the number of YouTube notifications
        sql = "SELECT count(`id`) as 'count' FROM `youtube_notifications` WHERE `discord_guild_id` = %s"
        res = self.db.select(sql, [discord_guild_id])

        # Check if the 'count' is equal to or greater than the YouTube notification limit
        if(res[0]['count'] >= self.get_youtube_limit(discord_guild_id)):
            # The limit has been reached or exceeded, return True
            return(True)

        # The limit has not been reached
        return(False)
