# Authors: @Travis-Owens, @Alireza-Sampour
# Date: 2020-10-12

# This class is used to lookup, parse, and find the channelId of a youtube
# channel from a url.
# The URL MUST be in one of two formats:
#   youtube.com/user/xxxxxx
#   youtube.com/channel/xxxxxx
# Preceding https:// or https://www. is accepted.

# Related Routes:
# - /youtube/manage/add
# - /youtube/manage/delete

import re
import requests
import json
import os

class youtube_channel_id(object):

    def __init__(self):
        pass

    def get_yt_channel_id(self, url):
        # This function will return the channel ID or the given URL.
        # If the function cannot find the channel ID, "None" will be returned.

        # If the url type is "/channel/", this function will return the channel ID
        # If the url type is "/user/", this function will return the username
        # if the url type is "/c/", this function will return the custom url vanity name
        channel = self.re_channel_from_url(url)

        if channel is None:
            # re_channel_from_url was unable to retrieve the channel_id, user,
            # or custom url from the input url
            return(None)

        # Depending on the url type, retrieve the channel ID
        if "/channel/" in url:
            # channel equals the Youtube channel ID
            return(channel)

        elif "/user/" in url:
            # channel equals the legacy username
            # Use the YouTube API to retrieve the channel ID from the username
            return(self.user_to_channel_id(channel))

        elif "/c/" in url:
            # channel equals the custom url vanity name
            # Use the Youtube API to search for the name
            return(self.custom_url_to_channel_id(channel))

        else:
            # Unable to parse the URL
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
        regex = r"(?:(?<=channel/)|(?<=c/)|(?<=user/))[^/?\s]+"

        # Use the search function to find the channel ID
        matches = re.search(regex, url, re.IGNORECASE)

        # Return the matched channel ID
        try:
            return (matches.group())
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

    def custom_url_to_channel_id(self, channel):
        # The YouTube Data API v3 does not explain how to convert a custom URL
        # to a channel ID. The only reliable method of getting the channel ID for
        # this URL type is to perform a serach and select the first channel.

        data = requests.get("https://www.googleapis.com/youtube/v3/search?part=id%2Csnippet&q=" + channel + "&type=channel&key=" + os.getenv('GCP_API_KEY').strip("\r"))

        data = json.loads(data.content.decode('utf-8'))

        channel_id = data['items'][0]['id']['channelId']

        return(channel_id)
