# Author: @Travis-Owens
# Date: 2021-01-13
# Desc: This route is used to recieve notifications about changes to the 'helix/users' endpoint.
#        Currently only the "twitch_username" field is tracked in the database.

import falcon
import json

from classes.twitch_management import twitch_management

class twitch_callback_users(object):
    def __init__(self):
        pass

    def on_get(self, req, resp, twitch_user_id=None):
        # Respond to challenge
        resp.status = falcon.HTTP_200   # Set response type
        resp.content_type = ['application/json']    # Set content_type
        resp.body = req.params['hub.challenge'] # Body of response

    def on_post(self, req, resp, twitch_user_id):

        try:
            data = json.loads(req.bounded_stream.read().decode())

            if 'display_name' in data['data'][0]:
                twitch_display_name = data['data'][0]['display_name']
                twitch_management(twitch_display_name,0,0).update_user(twitch_user_id, twitch_display_name)


        except Exception as e:
            resp.body = str(e)
