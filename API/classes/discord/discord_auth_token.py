# Author: @Travis-Owens
# Date: 2020-12-16
# Description: This file is used in the web authentication flow, used to retrieve
#  a oauth2 token from Discord.

import requests
import os
import json

from classes.data_handler import data_handler

class discord_auth_token(object):
    def __init__(self):
        pass

    def get_token(self, code):
        # This function will retrieve a discord oauth token using the code
        # Generated by the user during the auth flow
        # Query /api/oauth2/token

        url  = "https://discordapp.com/api/oauth2/token"
        body = {
            'client_id':os.getenv('DISCORD_CLIENT_ID').strip("\r"),
            'client_secret':os.getenv('DISCORD_CLIENT_SECRET').strip("\r"),
            'redirect_uri':os.getenv('DISCORD_REDIRECT_URI').strip("\r"),
            'grant_type':'authorization_code',
            'code':code,
        }
        token_resp  = requests.post(url, data=body)
        data        = token_resp.json()

        if(token_resp.status_code == 200):
            # Token successfully retrieved from Discord

            # Add token to database
            # Returns True or False, indicating success or failure
            db_status = self.insert_auth_token(data, code)

            # successfully obtained token
            resp = {
                'success':db_status,
                'code':code
            }

        else:
            # Could not obtain token
            resp = {
                'success':False,
                'code':code
            }

        return(resp)

    def validate_auth_code(self, code):
        # Checks if the provided code exist in the database, returns true or false

        db_obj = data_handler()

        input = [code]
        sql   = "SELECT `authorization_code` FROM `discord_auth` WHERE `authorization_code` = %s"

        db_select = db_obj.select(sql, input)

        if(len(db_select) == 0):
            return(False)
        else:
            return(True)

    def insert_auth_token(self, data, code):

        try:
            db_obj = data_handler()

            input = [None, None, code, data['access_token'], data['refresh_token'], data['scope'], data['token_type']]
            sql   = "INSERT INTO `discord_auth` VALUES (%s,%s,%s,%s,%s,%s,%s)"

            db_insert = db_obj.insert(sql, input)

            return(db_insert)

        except Exception as e:
            print(e)
            return(False)