# Author: @Travis-Owens
# Date:   2020-02-16
# Description: used for adding/deleting twitch channels from the db

import falcon
import json
import requests
import os

from classes.data_handler import data_handler

class twitch_management(object):
    def __init__(self, twitch_username, discord_channel_id):
        self.db     = data_handler()
        self.twitch = twitch_handler()

        self.twitch_username    = twitch_username
        self.discord_channel_id = discord_channel_id
        self.twitch_user_id     = self.twitch.get_twitch_user_id(twitch_username)


    def add(self):
        if(self.twitch_user_id == None):
            return("Twitch username is invalid!")

        if(len(self.db.defined_select('unique_twitch_notification', [self.twitch_username, self.discord_channel_id])) != 0):
            return("Notification already exist!")

        subscribe_status = self.twitch.subscribe(self.twitch_user_id)

        if(subscribe_status == True):
            db_status        = self.db.defined_insert('add_twitch_notification', [self.twitch_username, self.twitch_user_id, self.discord_channel_id])
        else:
            return("Error subscribing to twitch service!")

        if(db_status == True):
            return("Notification successfully added!")
        else:
            return("Error saving notifiaction to database!")


    def delete(self):
        if(self.twitch_user_id == None):
            return("Twitch username is invalid!")

        db_status = self.db.defined_delete('delete_twitch_notification', [self.twitch_username, self.twitch_user_id, self.discord_channel_id])

        if(db_status == True):
            return("Notification successfully removed!")
        else:
            return("Error removing notifiaction!")



class twitch_handler(object):
    def __init__(self):
        self.oauth_token = 'Bearer ' + data_handler().defined_select('twitch_oauth_token',input=None)[0]['setting_value']

    def get_twitch_user_id(self, twitch_username):
        # Using twitch helix api: convert twitch_username into twitch_user_id
        url = 'https://api.twitch.tv/helix/users?login=' + twitch_username

        headers = {
            'client-id': os.getenv('TWITCH_CLIENT_ID').strip("\r"),
            'Authorization': self.oauth_token
        }

        resp = requests.get(url, headers=headers)

        # Check http status code and ensure data is recieved
        if(resp.status_code == 200 and len(resp.json()['data']) > 0):
            return(resp.json()['data'][0]['id'])

        return None

    def update_subscription(self, mode, twitch_user_id):
        if(mode.lower() == 'subscribe' or mode.lower() == 'unsubscribe'):

            headers = {
                        'Content-Type' : 'application/json',
                        'client-id' : os.getenv('TWITCH_CLIENT_ID').strip("\r"),
                        'Authorization': self.oauth_token
                        }

            data = {"hub.mode":mode.lower(),
                "hub.topic":str("https://api.twitch.tv/helix/streams?user_id=" + twitch_user_id),
                "hub.callback":str(os.getenv('WEBHOOK_CALLBACK') + "/" + twitch_user_id),
                "hub.lease_seconds":"864000",
                "hub.secret":"top_secret",}

            r = requests.post('https://api.twitch.tv/helix/webhooks/hub', data=json.dumps(data), headers=headers)

            # print(r.content)
            if(r.status_code == 202):
                return(True)
            else:
                return(False)

    def subscribe(self, twitch_user_id):
        return(self.update_subscription('subscribe', twitch_user_id))
