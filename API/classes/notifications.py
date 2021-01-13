# Author: @Travis-Owens
# Date: 2021-01-12
# Desc: Used to retreive a list of notifications by discord_channel_id

from classes.data_handler import data_handler

class notifications(object):
    def __init__(self):
        self.db = data_handler()

    def get_twitch_notifications(self, discord_channel_id):
        # Return format:
        # [{'twitch_user_id':x,'twitch_username':y}, ... ]

        # Get Twitch User IDs
        sql  = "SELECT `twitch_user_id` FROM `twitch_notifications` WHERE `discord_channel_id` = %s"
        twitch_user_ids = data_handler().select(sql, [discord_channel_id])

        if(len(twitch_user_ids) == 0):
            # No twitch notifications found for the discord_channel_id
            return(None)

        # Flatten the twitch_user_ids dict into a list
        twitch_user_ids = list(map(lambda x : x['twitch_user_id'], twitch_user_ids))

        # Get Twitch Usernames
        sql = "SELECT `twitch_user_id`, `twitch_username` FROM `twitch_channels` WHERE `twitch_user_id` IN (%s)"
        # Inserts a '%s' for each element in the twitch_user_ids list
        sql = sql % ','.join(['%s'] * len(twitch_user_ids))

        twitch_data = data_handler().select(sql, tuple(twitch_user_ids))

        return(twitch_data)


    def get_youtube_notifications(self, discord_channel_id):
        # Return format:
        # [{'youtube_channel_id':x}, ...]

        # Get YouTube Channel IDs
        sql = "SELECT `yt_channel_id` as 'youtube_channel_id' FROM `youtube` WHERE `disc_channel_id` = %s"
        youtube_channel_ids = self.db.select(sql, [discord_channel_id])

        if(len(youtube_channel_ids) == 0):
            return(None)

        return(youtube_channel_ids)
