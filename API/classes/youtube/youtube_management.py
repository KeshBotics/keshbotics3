# Author: @Travis-Owens
# Date: 2020-10-11
# Description: This class is used to add/delete subscriptions from the database,
#              and subscribe to webhook notifications from YouTube.

# Related Routes:
# - /youtube/manage/add
# - /youtube/manage/delete

import requests
import os
import json

from classes.data_handler import data_handler
from classes.youtube.youtube_channel_id import youtube_channel_id

class youtube_management(object):
    def __init__(self):
        # Object for interacting with the database
        self.data_handler = data_handler()

    def subscribe(self, yt_channel_url, discord_guild_id, discord_channel_id):
        # Use the youtube_channel_id class to determine the YouTube channel ID
        # for the given URL.

        # Convert the yt_channel_url into a YouTube channel ID.
        yt_channel_id = youtube_channel_id().get_yt_channel_id(yt_channel_url)

        # If the youtube_channel_id is unable to parse the URL, return the error.
        if yt_channel_id is None:
            return({"status":"error", "code":400, "message":"Error unable to parse the URL!"})

        # Check if the yt_channel_id and discord_channel_id combination are unqiue.
        if(self.check_if_exist(yt_channel_id, discord_channel_id)):
            # The subscription to the YouTube channel in the Discord channel already exist.
            return({"status":"error", "code":400, "message":"Notification already exist!"})

        # Add notifcation to local databse
        yt_display_name = self.get_display_name(yt_channel_id)
        database_status = self.manage_databse_subscription("subscribe", yt_channel_id, yt_display_name, discord_channel_id, discord_guild_id)

        # Check if the local database insertion
        if database_status is False:
            # Error with the database
            return({"status":"error", "code":503, "message":"Error internal database failure!"})

        # Subscribe to the webhook for the given channel
        subscribe_status = self.manage_webhook_subscription("subscribe", yt_channel_id)

        # Check if the YouTube API subscription was successful
        if subscribe_status is False:
            # Error with YouTube API
            # return("Error: YouTube API error!")
            # This should not be returned to the user, create an internal
            # mechanism for handling this
            pass

        return({"status":"success", "code":200, "message":"Notification successfully added!"})

    def unsubscribe(self, yt_channel_url, discord_channel_id):
        # Use the youtube_channel_id class to determine the YouTube channel ID
        # for the given URL.

        # Convert the yt_channel_url into a YouTube channel ID.
        yt_channel_id = youtube_channel_id().get_yt_channel_id(yt_channel_url)

        # If the youtube_channel_id is unable to parse the URL, return the error.
        if yt_channel_id is None:
            return({"status":"error", "code":400, "message":"Error unable to parse the URL!"})

        # Remove the yt_channel and discord_channel_id combination from the database
        database_status = self.manage_databse_subscription("unsubscribe", yt_channel_id, discord_channel_id, None)

        # Ignore unsubscribing from the YouTube webhook, the lease will automatically expire,
        # and unsubscribing could create unintended results

        if database_status == False:
            # TODO: Implement methodolgy of notifiying developers about this issue.
            return({"status":"error", "code":503, "message":"Error removing notification from the database!"})
        else:
            return({"status":"success", "code":200, "message":"Notification successfully removed!"})


    def check_if_exist(self, yt_channel_id, discord_channel_id):
        # If the yt_channel_id and discord_channel_id already exist in the database
        # this function will return True, else it will return False.

        # Using data_handler class, create a SELECT query to find if the variable
        # combination exist.
        sql     = "SELECT * FROM `youtube_notifications` WHERE `yt_channel_id` = %s AND `discord_channel_id` = %s"
        values  = [yt_channel_id, discord_channel_id]
        resp    = self.data_handler.select(sql, values)

        if(len(resp) == 0):
            # If resp(list) is empty(0), the combination does not exist
            return(False)
        else:
            return(True)

    def manage_databse_subscription(self, mode, yt_channel_id, yt_display_name, discord_channel_id, discord_guild_id = None):
        # This function will add(INSERT) or delete(DELETE) subscriptions to/from the database.

        try:
            if(mode == "subscribe"):
                # Insert notification information
                values = [yt_channel_id, discord_guild_id, discord_channel_id]
                sql = "INSERT INTO `youtube_notifications` VALUES (NULL, %s, %s, %s)"
                res = self.data_handler.insert(sql, values)

                # If the channel ID is new/unique to the database, insert the id
                #  and display name into `youtube_channels`
                channel_res = self.data_handler.select("SELECT * FROM `youtube_channels` WHERE `yt_channel_id` =  %s", [yt_channel_id])

                if(len(channel_res) == 0):
                    self.data_handler.insert("INSERT INTO `youtube_channels` VALUES (NULL, %s, %s)", [yt_channel_id, yt_display_name])


            elif(mode == "unsubscribe"):
                values = [yt_channel_id, discord_channel_id]
                sql = "DELETE FROM `youtube_notifications` WHERE `yt_channel_id` = %s AND `discord_channel_id` = %s"
                res = self.data_handler.delete(sql, values)

            else:
                # "subscribe" and "unsubscribe" are hardcoded so this should never happen
                print("ERROR: Unknown mode in manage_databse_subscription")
                return(False)

            return(True)

        except Exception as e:
            print("manage_databse_subscription: " + str(e))
            return(False)


    def manage_webhook_subscription(self, mode, yt_channel_id):
        # This function subscribe/unsubscribe to/from notifications for the youtube
        # channel id given with the YouTube appspot API

        try:
            # Google/YouTube utilizes appspot to send webhook based notifications
            url = "https://pubsubhubbub.appspot.com/subscribe"

            # callback, topic, verify, and mode must be sent as a "form"
            payload = self.get_form_data(mode, yt_channel_id)

            # Currently, no headers are required.
            headers= {}

            # NOTE:  Figure out a better solution
            # timeout =1.xx is 100% a hack. Falcon only supports a single simultaneous
            # connection, the pubsubhubbub attemtps to reach /youtube/callback, however,
            # this current API request is blocking Falcon from responding.
            # Setting timeout to 1 sec will "ensure" that the payload POST data is sent,
            # and that the pubsubhubbub is able to reach the callback.
            response = requests.post(url, headers=headers, data = payload, timeout=1.0000000001)

            return(True)

        except requests.exceptions.ReadTimeout:
            # NOTE: See above
            return(True)
        except Exception as e:
            print("manage_webhook_subscription: " + str(e))
            return(False)

    def get_form_data(self, mode, yt_channel_id,):
        # The return dict contains the required variables to subscribe to the
        # appspot webhook.
        return({
            'hub.callback':os.getenv('YOUTUBE_CALLBACK').strip("\r"),
            'hub.topic':'https://www.youtube.com/xml/feeds/videos.xml?channel_id=' + yt_channel_id,
            'hub.verify':'sync',
            'hub.mode': mode
        })

    def get_display_name(self, yt_channel_id):
        # This function is used to retrieve the channel display name/title
        # of the associated yt_channel_id
        # NOTE: If a list is passed in for the argument 'yt_channel_id', this function
        # will return the data in a dictionary format (the raw snippet data). If a string is passed, this
        # function will only return the channel's display name (string).

        if type(yt_channel_id) is list:
            # convert list into string with values seperated by a comma
            # /youtube/v3/channels endpoint supports using a list of channel IDs.
            id = ",".join(yt_channel_id)
        else:
            id = yt_channel_id

        try:
            # Use the Google API to retreive the 'snippet' for the provided yt_channel_id
            data = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet&id=" + id + "&key=" + os.getenv('GCP_API_KEY').strip("\r"))
            data = json.loads(data.content.decode('utf-8'))

            if type(yt_channel_id) is list:
                # Return the snippet data for all requested channel IDs
                return(data)
            else:
                # Return the string value of the 'title' field
                return(data['items'][0]['snippet']['title'])

        except Exception as e:
            # Failed to retreive the youtube channel name
            return(None)

    def get_channel_ids(self):
        # Returns a unique list of Channel ID's stored in the database, returns a list of dicts
        data = self.data_handler.select("SELECT DISTINCT `yt_channel_id` FROM `youtube_channels`", [])

        # Flatten the dicts into a list
        return(list(map(lambda x : x['yt_channel_id'], data)))

    def update_display_names(self):
        # Will update the `yt_display_name` column in `youtube_channels`.
        # I don't think that the pubsubhubbub model supports sending webhooks
        # when a channel updates their name.

        yt_channel_ids = self.get_channel_ids()

        snippet_data  = self.get_display_name(yt_channel_ids)

        for channel in snippet_data['items']:
            yt_channel_id = channel['id']
            yt_display_name = channel['snippet']['title']
            self.data_handler.update("UPDATE `youtube_channels` SET `yt_display_name` = %s WHERE `yt_channel_id` = %s", [yt_display_name, yt_channel_id])

    def update_webhook_subs(self):
        # Will update the pubsubhubbub webhook subscription for each channel
        #  stored in the databse.

        # Get a list of the YouTube Channel IDs stored in the database
        yt_channel_ids = self.get_channel_ids()

        for channel_id in yt_channel_ids:
            self.manage_webhook_subscription('subscribe', channel_id)
