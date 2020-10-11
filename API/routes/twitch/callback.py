
import falcon
import json

from classes.discord_post import discord_post
from classes.data_handler import data_handler
from classes.twitch.stream_metrics import stream_metrics

class twitch_callback(object):
    def __init__(self):
        pass

    def on_get(self, req, resp, twitch_user_id=None):
        # Respond to challenge
        resp.status = falcon.HTTP_200   # Set response type
        resp.content_type = ['application/json']    # Set content_type
        resp.body = req.params['hub.challenge'] # Body of response

    def on_post(self, req, resp, twitch_user_id=None):

        try:
            data = json.loads(req.bounded_stream.read().decode())

            if 'user_id' in data['data'][0]:
                # Twitch user is online
                twitch_username         = data['data'][0]['user_name']
                # twitch_user_id          = data['data'][0]['user_id']
                twitch_thumbnail_url    = data['data'][0]['thumbnail_url']

                # is_streaming resloves an issue with twitch sending multiple stream objects
                # this prevents duplicate stream notifications
                is_streaming = data_handler().defined_select("is_streaming", twitch_user_id, False)

                if(is_streaming[0]['streaming'] == True):
                    # Streaming notification already sent
                    pass
                else:
                    # Notifcation has not been sent
                    discord_post_obj    = discord_post()
                    message             = discord_post_obj.prepare_twitch_message(twitch_username, twitch_thumbnail_url)
                    discord_channel_ids = data_handler().defined_select('discord_channels_by_twitch_user_id', [twitch_user_id], True)

                    discord_post_obj.post_message(message, discord_channel_ids)
                    stream_metrics().stream_start(twitch_user_id)
                    data_handler().defined_update('update_is_streaming', [1, twitch_user_id])


        except Exception as e:
            resp.body = str(e)
            # twitch user is offline
            stream_metrics().stream_stop(twitch_user_id)
            data_handler().defined_update('update_is_streaming', [0, twitch_user_id])
