# Author: Travis-Owens
# Date: 2020-05-07
# Desc: This is used to retrieve a new oauth2 token from twitch,
#  Updates the DB, and revokes the old token
# REF: https://dev.twitch.tv/docs/authentication/

import requests
import pymysql
import os

class twitch_oauth(object):
    def __init__(self):

        new_token = self.get_new_token()
        old_token = self.db_get_token()

        self.db_update_token(new_token)
        self.revoke_old_token(old_token)

    def get_new_token(self):
        # Using the Twitch OAuth2 route, reteive an access token
        try:
            twitch_token_url = 'https://id.twitch.tv/oauth2/token'

            params = {
                'client_id': os.getenv('TWITCH_CLIENT_ID'),
                'client_secret': os.getenv('TWITCH_SECRET'),
                'grant_type': 'client_credentials'
            }

            resp = requests.post(twitch_token_url, params=params)

            data = resp.json()

            return(data['access_token'])
        except Exception as e:
            pass

    def revoke_old_token(self, old_token):

        twitch_revoke_url = 'https://id.twitch.tv/oauth2/revoke'

        params = {
            'client_id': os.getenv('TWITCH_CLIENT_ID'),
            'token': old_token
        }

        resp = requests.post(twitch_revoke_url, params=params)

    # DATABASE
    def get_connection(self):
        return(pymysql.connect(host=os.getenv('DB_HOST'),
                                     user=os.getenv('DB_USER'),
                                     password=os.getenv('DB_PASS'),
                                     db=os.getenv('DB_NAME'),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor))

    def db_get_token(self):

        sql = "SELECT `setting_value` FROM `settings` WHERE `setting_key` = 'twitch_oauth_token'"

        connection = self.get_connection()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        data = cursor.fetchall()

        cursor.close()

        return(data[0]['setting_value'])


    def db_update_token(self, new_token):
        sql = "UPDATE `settings` SET `setting_value` = %s WHERE `setting_key` = 'twitch_oauth_token'"

        connection = self.get_connection()

        with connection.cursor() as cursor:
            cursor.execute(sql, [new_token])

        connection.commit()
        cursor.close()
