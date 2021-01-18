# Author: @Travis-Owens
# Date: 2020-10-17
# Description: This class is used to send messages (notifications) about YouTube
#               uploads to the appropriate Discord text-channels. The database is
#               structured as follows `id`, `yt_channel_id`, `disc_channel_id`.
#               When a new video ID is received, this class will find the
#               Discord channel IDs associated with the YouTube channel ID.

# Related Routes:
# - /youtube/callback

from classes.discord_post import discord_post
from classes.data_handler import data_handler


class youtube_notification(object):
    def __init__(self):
        self.data_handler = data_handler()

    def post_notification(self, yt_channel_id, yt_video_id, yt_video_author, yt_video_title):
        # Process the information received from the webhook callback

        # Check if notification was already sent
        # Duplicate POST checking, in testing some yt_video_ids were sent multiple times
        is_unique = self.check_for_duplicate(yt_video_id)

        if is_unique is False:
            # The given video id has already been processed, quit processing the request
            return

        # The given video id is new, insert it into the database
        self.insert_video_id(yt_video_id)

        # Select discord_channel_ids that have subscribed to yt_channel_id
        discord_channel_ids = self.get_discord_channel_ids(yt_channel_id)

        # post notifcation to discord
        # Prepare formated embed message
        message = self.prepare_discord_message(yt_video_id, yt_video_author, yt_video_title)
        discord_post().post_message(message, discord_channel_ids)

    def check_for_duplicate(self, yt_video_id):
        # The ID of each video is stored in the database to prevent duplication.
        # If the youtube video id is unique, this function will return True
        # If the youtube vidoe id has already been processed / had notification sent, this function will return false.

        sql     = "SELECT * FROM `youtube_submissions` WHERE `yt_video_id` = %s"
        values  = [yt_video_id]
        res     = self.data_handler.select(sql, values)

        if(len(res) == 0):
            # The video ID was not found in the database
            return(True)
        else:
            # The video ID is NOT unique
            return(False)

    def insert_video_id(self, yt_video_id):
        # This function will add the youtube video id to the databse `youtube_submissions`
        # This table is used to prevent duplicate notifications

        sql     = "INSERT INTO `youtube_submissions` VALUES(NULL, %s)"
        values  = [yt_video_id]
        self.data_handler.insert(sql, values)

        return


    def get_discord_channel_ids(self, yt_channel_id):
        # This function will search the databse for discord_channel_ids that have subscribed to yt_channel_id

        sql     = "SELECT `disc_channel_id` FROM `youtube` WHERE `yt_channel_id` = %s"
        values  = [yt_channel_id]
        data    = data_handler().select(sql, values)

        # Flatten the dict to only the keys (disc_channel_id)
        return(list(map(lambda x : x['disc_channel_id'], data)))

    def prepare_discord_message(self, yt_video_id, yt_video_author, yt_video_title):
        # Embeded message for Discord
        message = {
              # "content": ,
              "embed": {
                "title": "https://www.youtube.com/watch?v=" + yt_video_id,
                "description": "",
                "url": "https://www.youtube.com/watch?v=" + yt_video_id,
                "color": 9442302,
                "timestamp": "",
                "footer": {
                  "icon_url": "https://cdn.discordapp.com/avatars/532575955324239882/653f3b3749c3da11947a70881d675160.png?size=256",
                  "text": "KeshBotics"
                },
                "thumbnail": {
                  # "url": ""
                },
                "image": {
                  "url": "https://i.ytimg.com/vi/" + yt_video_id + "/hq720.jpg"
                },
                "author": {
                  "name": yt_video_author,
                  "url": "https://www.youtube.com/watch?v=" + yt_video_id,
                  "icon_url": "https://cdn.discordapp.com/avatars/532575955324239882/653f3b3749c3da11947a70881d675160.png?size=256"
                },
                "fields": [
                          {
                            "name": yt_video_title,
                            "value": '\u200B'
                          }
                        ]
              }
            }

        return(message)
