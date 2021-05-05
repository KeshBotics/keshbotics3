# Authors: @Travis-Owens, @Alireza-Sampour
# Date: 2020-10-12

# This class is used to lookup, parse, and find the channelId of a youtube
# channel from a url.
# The URL MUST be in one of the following formats:
#   youtube.com/user/<identifier>         # Legacy username
#   youtube.com/channel/<identifier>      # ID-based
#   youtube.com/c/<identifier>            # Custom
#   youtube.com/<identifier>              # Shortened, either Custom or Legacy username
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

        # This function uses regex to determine the channel type and identifier value
        channel = self.re_channel_from_url(url)

        # Handle the various channel types accordingly
        if(channel['type'] == "channel"):
            # type is "/channel/", the value is a channel ID
            return(channel['value'])

        elif(channel['type'] == "user"):
            # type is "/user/", the value is a username
            return(self.user_to_channel_id(channel['value']))

        elif(channel['type'] == "c"):
            # type is "/c/", the value is custom name
            return(self.custom_url_to_channel_id(channel['value']))

        elif(channel['type'] == "shortened"):
            # type is "/", the value is either custom name or username
            return(self.shortened_url(channel['value']))

        # Unexpected channel type/ Regex function was unable to find a channel type and identifier value
        return(None)

    def re_channel_from_url(self, url):
        # This function will parse the various YouTube channel URL's and return
        # a dictionary with the URL type and the identifier value.
        # Return format:
        #  {'type':<"channel"|"c"|"user"|"shortened">, "value":<identifier>}

        # Ensure that hostname is YouTube
        # This isn't fool proof, extremely basic checking
        if "youtube" not in url:
            return(None)

        # Regular expression to select the necessary information from the URL
        # re.findall will return a list:
        # "[<type>, <identifier]" or ["identifier"](shortened URL)
        regex = r"(?:(?<=channel\/)|(?<=c\/)|(?<=user\/)|(?<=.com\/))([^/?\s]+)"
        matches = re.findall(regex, url, re.IGNORECASE)

        if(len(matches) == 0):
            # A match was not found
            return(None)

        elif(len(matches) == 1):
            # URL type is shortened "/<identifier"
            return({"type":"shortened","value":matches[0]})

        elif(len(matches) == 2):
            # URL type is channel, user, or c
            return({"type":matches[0],"value":matches[1]})

        # Unexpected matches length
        return(None)

    def user_to_channel_id(self, channel):
        # URL TYPE: "/user/x"
        # This function will use the "YouTube Data API v3" to retreive the
        # channel ID from the given
        try:
            data = requests.get("https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=" + channel + "&key=" + os.getenv('GCP_API_KEY').strip("\r"))

            data = json.loads(data.content.decode('utf-8'))

            # If username is not found, KeyError exception will trigger
            channel_id = data['items'][0]['id']

            return(channel_id)

        except KeyError:
            # Username was not found
            return(None)

        except Exception as e:
            # Unexpected Exception
            return(None)

    def custom_url_to_channel_id(self, channel):
        # NOTE: This performs a search and returns the first channel found,
        #           This may not always be the intended channel.

        # URL TYPE: "/c/x"
        # The YouTube Data API v3 does not explain how to convert a custom URL
        # to a channel ID. This function will search for the custom name (vanity URL)
        # via the API's search route. This will typically return a list of channels,
        # in order to select the correct channel.. the channels API route needs to be called
        # and the field ['items'][i]['snippet']['customUrl'] needs to be compared to the value
        # given in the function arguments.

        search = requests.get("https://www.googleapis.com/youtube/v3/search?part=id%2Csnippet&q=" + channel + "&type=channel&key=" + os.getenv('GCP_API_KEY').strip("\r"))
        search = json.loads(search.content.decode('utf-8'))

        return(search['items'][0]['id']['channelId'])

    def _not_implemented_custom_url_to_channel_id(self, channel):
        # NOTE: Some edge cases will break this implementation
        #  EX: https://www.youtube.com/RandallsRelaxation

        # URL TYPE: "/c/x"
        # The YouTube Data API v3 does not explain how to convert a custom URL
        # to a channel ID. This function will search for the custom name (vanity URL)
        # via the API's search route. This will typically return a list of channels,
        # in order to select the correct channel.. the channels API route needs to be called
        # and the field ['items'][i]['snippet']['customUrl'] needs to be compared to the value
        # given in the function arguments.

        try:
            # Perform a search for the custom URL name, in a vast majority of
            # cases the correct channel will be returned in this search
            search = requests.get("https://www.googleapis.com/youtube/v3/search?part=id%2Csnippet&q=" + channel + "&type=channel&key=" + os.getenv('GCP_API_KEY').strip("\r"))
            search = json.loads(search.content.decode('utf-8'))

            # The previous query will return a list of channels
            # Iterate over the resulting channels and fetch the snippet for each.
            # compare the 'channel' value given in this functions arguments to the
            # 'customUrl' field. A match indicates the correct channel has been found.
            for i in search['items']:
                channel_id = i['id']['channelId']

                channel_data = requests.get("https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=" + channel_id + "&key=" + os.getenv('GCP_API_KEY').strip("\r"))
                channel_data = json.loads(channel_data.content.decode('utf-8'))

                # Compare the given custom channel url to the customUrl field
                try:
                    if(channel.lower() == channel_data['items'][0]['snippet']["customUrl"].lower()):
                        # The correct channel has been found
                        return(channel_id)

                except:
                    # The if statement could create a keyError exception
                    # Not all channels will have the customUrl field
                    pass

            # Failed to find a channel ID of the given custom URL name
            return(None)

        except KeyError:
            # custom URL was not found
            return(None)

        except Exception as e:
            print(e)
            # Unexpected Exception
            return(None)

    def shortened_url(self, identifier):
        # URL TYPE: "/x"
        # Both "/c/x" and "/user/x" can be shortened to "/x".
        # "/user/x" can only be shortened to this if the "x"(Custom url) in "/c/x" has not
        #  been claimed.
        # REF: https://support.google.com/youtube/answer/6180214?hl=en

        # Check if identifier is a claimed as a custom URL
        custom_url_channel_id = self.custom_url_to_channel_id(identifier)

        if custom_url_channel_id is not None:
            # The identifier is a custom URL
            return(custom_url_channel_id)

        # Check if identifier is username
        user_url_channel_id = self.user_to_channel_id(identifier)

        if user_url_channel_id is not None:
            # The identifier is a username
            return(user_url_channel_id)

        # Unable to determine if the identifier belongs to a YouTube channel
        return(None)
