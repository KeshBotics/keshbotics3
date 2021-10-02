# Author: @Travis-Owens
# Date:   2020-02-16
# Description: used for adding/deleting twitch channels from the db

# Related Routes:
# - /twitch/manage/add
# - /twitch/manage/delete

import falcon
import json
import requests
import os

from classes.data_handler import data_handler
from classes.event_logging.event_logging import get_logger
from classes.discord_post import discord_post
from classes.notification_limit import notification_limit

class twitch_management(object):
    def __init__(self, twitch_username, discord_guild_id, discord_channel_id):
        self.db     = data_handler()
        self.twitch = twitch_handler()

        self.twitch_username    = twitch_username
        self.discord_guild_id   = discord_guild_id
        self.discord_channel_id = discord_channel_id
        self.twitch_user_id     = self.twitch.get_twitch_user_id(twitch_username)


    def add(self):
        # Used to add a new notifcation to the database
        # 1. Check if Twitch User ID is present
        # 2. Check if the notifcation already exist
        # 3. Subscribe to the twitch notifcation webhook
        # 4. Insert the twitch channel to `twitch_channels` table
        # 5. Insert the notifcation parameters to `twitch_notifications` table

        # Check if the discord_guild_id has reached the notification limit
        if(notification_limit().twitch_limit_reached(self.discord_guild_id)):
            # The limit has been reached
            return({"status":"error", "code":403, "message":"Notification limit has been reached!"})

        # Check if twitch_user_id is present
        if(self.twitch_user_id is None):
            return({"status":"error", "code":400, "message":"Twitch username is invalid!"})

        # Check if notification already exist in the database
        check_notification = self.db.select('SELECT * FROM `twitch_notifications` WHERE `twitch_user_id` = %s AND `discord_channel_id` = %s', [self.twitch_user_id, self.discord_channel_id])
        if(len(check_notification) != 0):
            return({"status":"error", "code":400, "message":"Notification already exist!"})

        # Subscribe to the Twitch webhook notification
        subscribe_status = self.twitch.subscribe(self.twitch_user_id)

        # Check if the subscription failed
        if not subscribe_status:
            return({"status":"error", "code":503, "message":"Error subscribing to twitch service!"})

        # Insert the twitch user and the notification parameters to the database
        # Add channel to `twitch_channels`.
        # Check if the twitch_user_id exist in the database, add if not
        channel_exist = self.db.select('SELECT `twitch_user_id` FROM `twitch_channels` WHERE `twitch_user_id` = %s', [self.twitch_user_id])
        if(len(channel_exist) == 0):
            # The Twitch user ID does not exist in the database
            self.db.insert('INSERT INTO `twitch_channels` VALUES (%s, %s, %s)', [self.twitch_user_id, self.twitch_username, 0])

        # Add notification parameters to `twitch_notifications`
        db_status = self.db.insert('INSERT INTO `twitch_notifications` VALUES (%s, %s, %s, %s)', [None, self.twitch_user_id, self.discord_guild_id, self.discord_channel_id])

        if db_status:
            return({"status":"success", "code":200, "message":"Notification successfully added!"})
        else:
            return({"status":"error", "code":503, "message":"Error saving notifiaction to database!"})


    def delete(self):
        # Used to remove a notification from the database
        # 1. Check if Twitch User ID is present
        # 2. Delete the notifcation from the database
        # NOTE: Obsolete Twitch channels will be removed via CRON task.
        # NOTE: Obsolete Twitch webhook subscriptions will expire naturally

        if(self.twitch_user_id == None):
            return({"status":"error", "code":400, "message":"Twitch username is invalid!"})

        db_status = self.db.delete('DELETE FROM `twitch_notifications` WHERE `twitch_user_id` = %s AND `discord_channel_id` = %s', [self.twitch_user_id, self.discord_channel_id])

        if(db_status == True):
            return({"status":"success", "code":200, "message":"Notification successfully removed!"})
        else:
            return({"status":"error", "code":503, "message":"Error removing notification!"})

    def update_user(self, twitch_user_id, twitch_display_name):
        # Used to updated twitch_usernames
        sql = "UPDATE `twitch_channels` SET `twitch_username` = %s WHERE `twitch_user_id` = %s"
        db_status = self.db.update(sql, [twitch_display_name, twitch_user_id])


class twitch_handler(object):
    def __init__(self):
        # Fetch twitch_oauth_token from `settings` DB, and then prepend 'Bearer'
        twitch_oauth_token = data_handler().select('SELECT `setting_value` FROM `settings` WHERE `setting_key` = "twitch_oauth_token"', None)[0]['setting_value']
        self.twitch_oauth_token = 'Bearer ' + twitch_oauth_token

    def get_twitch_user_id(self, twitch_username):
        # Using twitch helix api: convert twitch_username into twitch_user_id
        url = 'https://api.twitch.tv/helix/users?login=' + twitch_username

        headers = {
            'client-id': os.getenv('TWITCH_CLIENT_ID').strip("\r"),
            'Authorization': self.twitch_oauth_token
        }

        resp = requests.get(url, headers=headers)

        # Check http status code and ensure data is recieved
        if(resp.status_code == 200 and len(resp.json()['data']) > 0):
            return(resp.json()['data'][0]['id'])

        return None

    def update_subscription(self, mode, twitch_user_id):
        if(mode.lower() == 'subscribe' or mode.lower() == 'unsubscribe'):
            # TODO: update to eventsub



            headers = {
                        'Content-Type' : 'application/json',
                        'client-id' : os.getenv('TWITCH_CLIENT_ID').strip("\r"),
                        'Authorization': self.twitch_oauth_token
                        }

            data = {"hub.mode":mode.lower(),
                "hub.topic":str("https://api.twitch.tv/helix/streams?user_id=" + twitch_user_id),
                "hub.callback":str(os.getenv('API_URL') + "/twitch/callback/streams/" + twitch_user_id),
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

    def event(self, data):
        # This function is called when Twitch sends a webhook callback

        event = data['event']

        try:
            # store/check event["id"]; Twitch creates a unique ID for each event
            #  Sometimes the same event can be delivered multiple times. This prevents
            #  the event from being processed multiple times.
            sql = "SELECT event_id FROM `twitch_event_ids` WHERE `event_id` = %s"
            res = data_handler().select(sql, [event["event_id"]])

            if(len(res) != 0):
                # Event has already been published
                return
            else:
                # New event, add to the database
                sql = "INSERT INTO `twitch_event_ids` (`event_id`) VALUES (%s)"
                data_handler().insert(sql, [event["event_id"]])


            if(event["type"] == "live"):
                # Channel is now live

                # Update live status in database
                sql = "UPDATE `twitch_channels` SET `streaming` = 1 WHERE `twitch_user_id` =  %s"
                data_handler().update(sql, [event['broadcaster_user_id']])

                # Format thumbnail URL
                twitch_thumbnail_url = "https://static-cdn.jtvnw.net/previews-ttv/live_user_" + event["broadcaster_login_name"]  + "-640x360.jpg"

                # Prepare and Send discord message
                discord_post_obj    = discord_post()
                message             = discord_post_obj.prepare_twitch_message(event["broadcaster_login_name"], twitch_thumbnail_url)
                discord_channel_ids = data_handler().select('SELECT DISTINCT `discord_channel_id` FROM `twitch_notifications` WHERE `twitch_user_id`=%s', [event["broadcaster_user_id"]])
                discord_channel_ids = list(map(lambda x : x['discord_channel_id'], discord_channel_ids)) # FLatten results into a list
                discord_post_obj.post_message(message, discord_channel_ids)

            elif(event["type"] == "offline"):

                # Set streaming status to false
                sql = "UPDATE `twitch_channels` SET `streaming` = 0 WHERE `twitch_user_id` = %s"
                data_handler().update(sql, [event['broadcaster_user_id']])

        except Exception as e:
            get_logger().error(e, exc_info=True)
