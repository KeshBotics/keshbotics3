# Author: @Travis-Owens
# Date:   2020-02-16
# Description: The Twitch API will send a POST request to this route with
#               details about a Twitch user's live stream. The POST data does not
#               contain the twitch_user_id, to create clarity the twitch_user_id is
#               appended to the API route {twitch_user_id}. When a request is recieved
#               the necessary information is extracted, messages sent to the appropriate
#               discord channels, and start/stop times added to the stream metrics database
#               table. Additionally, when the live stream has concluded, Twitch will
#               send an empty json object. Because this application appends the
#               twitch_user_id to the callback this empty object can be correlated.
#
#               In some cases, Twitch will send multiple notifications about a
#               single live stream. This class attempts to mitigate sending the
#               same notification multiple times.

# Related Routes:
# - /twitch/callback/streams/{twitch_user_id}

import falcon
import json

from classes.event_logging.event_logging import get_logger
from classes.discord_post import discord_post
from classes.data_handler import data_handler
from classes.twitch_management import twitch_handler
from classes.twitch.stream_metrics import stream_metrics

class twitch_callback_streams(object):
    def __init__(self):
        pass

    def on_get(self, req, resp, twitch_user_id=None):
        # Respond to challenge
        resp.status = falcon.HTTP_200   # Set response type
        resp.content_type = ['application/json']    # Set content_type
        resp.body = req.params['hub.challenge'] # Body of response

    def on_post(self, req, resp, twitch_user_id=None):

        try:
            # Load the JSON data
            data = json.loads(req.bounded_stream.read().decode())

            # Check if the request is a challenge
            if "challenge" in data:
                # Respond to the challenge
                resp.status = falcon.HTTP_200
                resp.body = data["challenge"]

                # This request is not an actually notification, stop processing
                return

            if "event" in data:
                # Call the twitch_handler event function
                twitch_handler().event(data)

        except Exception as e:
            get_logger().error(e, exc_info=True)
