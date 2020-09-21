# Author: @Travis-Owens
# Date:  2020-02-19
# Description: Subribes to twitch webhook

import pymysql
import requests
import json
import os

class twitch_subscribe(object):
    def __init__(self):
        self.users = self.get_unqiue_twitch_users()

        for user in self.users:
            self.update_subscription('subscribe', user['twitch_user_id'])

        self.db_log_cron_event()

    def get_connection(self):
        return(pymysql.connect(host=os.getenv('DB_HOST'),
                                     user=os.getenv('DB_USER'),
                                     password=os.getenv('DB_PASS'),
                                     db=os.getenv('DB_NAME'),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor))

    def get_unqiue_twitch_users(self):
        sql = "SELECT DISTINCT `twitch_user_id` FROM `twitch`"

        connection = self.get_connection()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        return(cursor.fetchall())


    def update_subscription(self, mode, twitch_user_id):
        if(mode.lower() == 'subscribe' or mode.lower() == 'unsubscribe'):

            twitch_oauth_token = 'Bearer ' + self.db_get_token()

            headers = {'Content-Type' : 'application/json', 'Client-ID' : os.getenv('TWITCH_CLIENT_ID'), 'Authorization':twitch_oauth_token}
            data = {"hub.mode":mode.lower(),
                "hub.topic":str("https://api.twitch.tv/helix/streams?user_id=" + twitch_user_id),
                "hub.callback":str(os.getenv('WEBHOOK_CALLBACK') + "/" + twitch_user_id),
                "hub.lease_seconds":"864000",
                "hub.secret":"top_secret",}

            r = requests.post('https://api.twitch.tv/helix/webhooks/hub', data=json.dumps(data), headers=headers)

            if(r.status_code == 202):
                return(True)
            else:
                print(r.content)
                return(False)

    def db_get_token(self):

        sql = "SELECT `setting_value` FROM `settings` WHERE `setting_key` = 'oauth_token'"

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
