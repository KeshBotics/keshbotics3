# Author: @Travis-Owens
# Date: 2020-10-11
# Description: This class is used to add/delete subscriptions from the database,
#              and subscribe to webhook notifications from YouTube.

# Related Routes:
# - /youtube/manage/add
# - /youtube/manage/delete

import requests
import os

from classes.data_handler import data_handler
from classes.youtube.youtube_channel_id import youtube_channel_id

class youtube_management(object):
    def __init__(self):
        # Object for interacting with the database
        self.data_handler = data_handler()

    def subscribe(self, yt_channel_url, disc_channel_id):
        # Use the youtube_channel_id class to determine the YouTube channel ID
        # for the given URL.

        # Convert the yt_channel_url into a YouTube channel ID.
        yt_channel_id = youtube_channel_id().get_yt_channel_id(yt_channel_url)

        # If the youtube_channel_id is unable to parse the URL, return the error.
        if yt_channel_id is None:
            return("Error unable to parse the URL!")

        # Check if the yt_channel_id and disc_channel_id combination are unqiue.
        if(self.check_if_exist(yt_channel_id, disc_channel_id)):
            # The subscription to the YouTube channel in the Discord channel already exist.
            return("Notification already exist!")

        # Add notifcation to local databse
        database_status = self.manage_databse_subscription("subscribe", yt_channel_id, disc_channel_id)

        # Check if the local database insertion
        if database_status is False:
            # Error with the database
            return("Error internal database failure!")

        # Subscribe to the webhook for the given channel
        # # TODO: figure out timing issue
        subscribe_status = self.manage_webhook_subscription("subscribe", yt_channel_id)

        # Check if the YouTube API subscription was successful
        if subscribe_status is False:
            # Error with YouTube API
            # return("Error: YouTube API error!")
            # This should not be returned to the user, create an internal
            # mechanism for handling this
            pass

        return("Notification successfully added!")

    def unsubscribe(self, yt_channel_url, disc_channel_id):
        # Use the youtube_channel_id class to determine the YouTube channel ID
        # for the given URL.

        # Convert the yt_channel_url into a YouTube channel ID.
        yt_channel_id = youtube_channel_id().get_yt_channel_id(yt_channel_url)

        # If the youtube_channel_id is unable to parse the URL, return the error.
        if yt_channel_id is None:
            return("Error unable to parse the URL!")

        # Remove the yt_channel and disc_channel_id combination from the database
        database_status = self.manage_databse_subscription("unsubscribe", yt_channel_id, disc_channel_id)

        # Ignore unsubscribing from the YouTube webhook, the lease will automatically expire,
        # and unsubscribing could create unintended results

        if database_status == False:
            # TODO: Implement methodolgy of notifiying developers about this issue.
            return("Error removing notification from the database!")
        else:
            return("Notification successfully removed!")


    def check_if_exist(self, yt_channel_id, disc_channel_id):
        # If the yt_channel_id and disc_channel_id already exist in the database
        # this function will return True, else it will return False.

        # Using data_handler class, create a SELECT query to find if the variable
        # combination exist.
        sql     = "SELECT * FROM `youtube` WHERE `yt_channel_id` = %s AND `disc_channel_id` = %s"
        values  = [yt_channel_id, disc_channel_id]
        resp    = self.data_handler.select(sql, values)

        if(len(resp) == 0):
            # If resp(list) is empty(0), the combination does not exist
            return(False)
        else:
            return(True)

    def manage_databse_subscription(self, mode, yt_channel_id, disc_channel_id):
        # This function will add(INSERT) or delete(DELETE) subscriptions to/from the database.

        values = [yt_channel_id, disc_channel_id]
        try:
            if(mode == "subscribe"):
                sql = "INSERT INTO `youtube` VALUES(NULL, %s, %s)"
                res = self.data_handler.insert(sql, values)

            elif(mode == "unsubscribe"):
                sql = "DELETE FROM `youtube` WHERE `yt_channel_id` = %s AND `disc_channel_id` = %s"
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

            # TODO: Figure out a better solution
            # timeout =1.xx is 100% a hack. Falcon only supports a single simultaneous
            # connection, the pubsubhubbub attemtps to reach /youtube/callback, however,
            # this current API request is blocking Falcon from responding.
            # Setting timeout to 1 sec will "ensure" that the payload POST data is sent,
            # and that the pubsubhubbub is able to reach the callback.
            response = requests.post(url, headers=headers, data = payload, timeout=1.0000000001)

            print(response.content)
            return(True)

        except requests.exceptions.ReadTimeout:
            # TODO: See above
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
