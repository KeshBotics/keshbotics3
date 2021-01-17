# Author: @Travis-Owens
# Date:  2020-02-19
# Description: Subribes to twitch webhook events. 'helix/streams' and 'helix/users'

import pymysql
import requests
import json
import os

class twitch_subscribe(object):
    def __init__(self):
        # Retrieves a unique list of of twitch user ID's from the 'twitch_channels' table
        self.users = self.get_unqiue_twitch_users()

        # Update both webhook subscriptions for each user ID
        for user in self.users:
            self.update_subscription(str(user['twitch_user_id']))

        # Adds an entry to the database indicating that this task is active
        self.db_log_cron_event()

    def get_connection(self):
        return(pymysql.connect(host=os.getenv('DB_HOST'),
                                     user=os.getenv('DB_USER'),
                                     password=os.getenv('DB_PASS'),
                                     db=os.getenv('DB_NAME'),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor))

    def get_unqiue_twitch_users(self):
        sql = "SELECT DISTINCT `twitch_user_id` FROM `twitch_channels`"

        connection = self.get_connection()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        return(cursor.fetchall())


    def update_subscription(self, twitch_user_id):

        # Get the oauth token from the DB and prepend 'Bearer'
        twitch_oauth_token = 'Bearer ' + self.db_get_token()

        # Headers and data required for creating/updating a subscription to a Twitch webhook event
        # 'hub.topic' and 'hub.callback' are set accordingly for each request ('streams' and 'users')
        # '864000' is the maximum allowed time for a lease (240 hours).
        headers = {'Content-Type' : 'application/json', 'Client-ID' : os.getenv('TWITCH_CLIENT_ID'), 'Authorization':twitch_oauth_token}
        data = {"hub.mode":"subscribe",
                "hub.topic":None,
                "hub.callback":None,
                "hub.lease_seconds":"864000",
                "hub.secret":"top_secret"
                }

        # Subscribe to the 'helix/streams' endpoint, used for stream notifications
        data["hub.topic"]    = str("https://api.twitch.tv/helix/streams?user_id=" + twitch_user_id)
        data["hub.callback"] = str(os.getenv('API_URL') + "/twitch/callback/streams/" + twitch_user_id)
        r = requests.post('https://api.twitch.tv/helix/webhooks/hub', data=json.dumps(data), headers=headers)

        # Subscribe to the 'helix/users' endpoint, used for tracking username changes
        data["hub.topic"]    = str("https://api.twitch.tv/helix/users?id=" + twitch_user_id)
        data["hub.callback"] = str(os.getenv('API_URL') + "/twitch/callback/users/" + twitch_user_id)
        r = requests.post('https://api.twitch.tv/helix/webhooks/hub', data=json.dumps(data), headers=headers)


    def db_get_token(self):

        sql = "SELECT `setting_value` FROM `settings` WHERE `setting_key` = 'twitch_oauth_token'"

        connection = self.get_connection()

        with connection.cursor() as cursor:
                cursor.execute(sql)

        data = cursor.fetchall()

        cursor.close()

        return(data[0]['setting_value'])

    def db_log_cron_event(self):
        sql = "INSERT INTO `cron_event` VALUES (0, null)"

        connection = self.get_connection()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        connection.commit()
        connection.close()

    def get_connection(self):
        return(pymysql.connect(host=os.getenv('DB_HOST'),
                                     user=os.getenv('DB_USER'),
                                     password=os.getenv('DB_PASS'),
                                     db=os.getenv('DB_NAME'),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor))
