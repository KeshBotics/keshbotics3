# Author: @Travis-Owens
# Date: 2020-10-12

# This class is used to lookup, parse, and find the channelId of a youtube
# channel from a url.
# The URL MUST be in one of two formats:
#   youtube.com/user/xxxxxx
#   youtube.com/channel/xxxxxx
# Preceding https:// or https://www. is accepted.

import re
import requests
import json

class youtube_channel_id(object):

    def __init__(self):
        pass

    def get_yt_channel_id(self, url):
        # This function will return the channel ID or the given URL.
        # If the function cannot find the channel ID, "None" will be returned.

        # Determine if the URL is a /user/ or /channel/ URL
        url_type = self.get_url_type(url)

        # If url_type is not "user" or "channel", this function will be
        # unable to determine the channel ID.
        if url_type is None:
            return(None)

        # If the url_type is "channel", this function will return the channel ID
        # If the url_type is "user", this function will return the username
        channel = self.re_channel_from_url(url)

        if url_type is "channel":
            # Use the regex function to select the channel ID from the URL.
            return(channel)

        elif url_type is "user":
            # Use the YouTube API to retrieve the channel ID from the username
            return(self.user_to_channel_id(channel))

    def get_url_type(self, url):
        if 'user' in url:
            return("user")
        elif 'channel' in url:
            return("channel")
        else:
            return(None)

    def re_channel_from_url(self, url):
        # This fucntion will use regex to parse the channel ID OR username from the URL
        # Ex: https://www.youtube.com/channel/exampleid
        # "exampleid" will be returned
        # Ex: https://www.youtube.com/user/exampleuser
        # "exampleuser" will be returned
        # .split("/") could be used, however, some URL's may contain arguments
        # after the channel ID.

        # Regular expression for selecting the channel ID
        # Look at: https://regex101.com/r/5TBgN1/1 for more information
        regex = r"^(?:https?:\/\/)?(?:(?:www|gaming)\.)?youtube\.com\/(?:channel\/|(?:user\/)?)([a-z\-_0-9]+)\/?(?:[\?#]?.*)"

        # Use the search function to find the channel ID
        matches = re.search(regex, url, re.IGNORECASE)

        # Return the matched channel ID
        try:
            return(matches[1])
        except:
            # In the event that the regex fails to find a channel ID in the URL
            return(None)

    def user_to_channel_id(self, channel):
        # This function will use the "YouTube Data API v3" to retreive the
        # channel ID from the given
        
        data = requests.get("https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=" + channel + "&key=" + os.getenv('GCP_API_KEY').strip("\r"))

        data = json.loads(data.content)

        channel_id = data['items'][0]['id']

        return(channel_id)
