# Author: @Travis-Owens
# Date: 2020-10-11
# Description: This class is used to subscribe and unsubscribe from the YouTube
#               webhook POST callbacks.

import requests

from classes.youtube.youtube_channel_id import youtube_channel_id

class youtube_management(object):
    def __init__(self):
        pass

    def subscribe(self, yt_channel_url):

        # Use the youtube_channel_id class to determine the YouTube channel ID
        # for the given URL.
        channel_id = youtube_channel_id().get_yt_channel_id(yt_channel_url)


    def unsubscribe(self, yt_channel_url):

        # Use the youtube_channel_id class to determine the YouTube channel ID
        # for the given URL.
        channel_id = youtube_channel_id().get_yt_channel_id(yt_channel_url)


    def get_form_data(self, yt_channel_id, mode):
        return({
            'hub.callback':'http://dev.api.vahkesh.com/youtube/callback',
            'hub.topic':'https://www.youtube.com/xml/feeds/videos.xml?channel_id=' + yt_channel_id,
            'hub.verify':'sync',
            'hub.mode': mode
        })
