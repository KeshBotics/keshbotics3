# Author: @Travis-Owens
# Date:  2020-10-17
# Description: Re-Subscribes to the YouTube webhook notifications

import pymysql
import os
import requests

class youtube_subscribe(object):
    def __init__(self):
        # A list of unique YouTube channel IDs from the database
        youtube_channel_ids = self.get_channel_ids()

        # Iterate over the list of channel IDs and re-subscribe to the webhook
        for channel_id in youtube_channel_ids:
            self.manage_webhook_subscription("subscribe", channel_id['yt_channel_id'])

    def get_channel_ids(self):
        sql = "SELECT DISTINCT `yt_channel_id` FROM `youtube`"

        conn = self.get_connection()

        with conn.cursor() as cursor:
            cursor.execute(sql)

        youtube_channel_ids = cursor.fetchall()

        cursor.close()

        return(youtube_channel_ids)


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

            # NOTE: Figure out a better solution
            # timeout =1.xx is 100% a hack. Falcon only supports a single simultaneous
            # connection, the pubsubhubbub attemtps to reach /youtube/callback, however,
            # this current API request is blocking Falcon from responding.
            # Setting timeout to 1 sec will "ensure" that the payload POST data is sent,
            # and that the pubsubhubbub is able to reach the callback.
            response = requests.post(url, headers=headers, data = payload, timeout=1.0000000001)

        except requests.exceptions.ReadTimeout:
            return(True)
        except Exception as e:
            print("manage_webhook_subscription: " + str(e))
            return(False)

    def get_form_data(self, mode, yt_channel_id,):
        return({
            'hub.callback':os.getenv('YOUTUBE_CALLBACK').strip("\r"),
            'hub.topic':'https://www.youtube.com/xml/feeds/videos.xml?channel_id=' + yt_channel_id,
            'hub.verify':'sync',
            'hub.mode': mode
        })


    def get_connection(self):
        return(pymysql.connect(host=os.getenv('DB_HOST').strip("\r"),
                                     user=os.getenv('DB_USER').strip("\r"),
                                     password=os.getenv('DB_PASS').strip("\r"),
                                     db=os.getenv('DB_NAME').strip("\r"),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor))
