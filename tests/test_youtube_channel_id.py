# Author: @Travis-Owens
# Date: 2021-03-18
# Desc: This class is used to test the class located at: "API/classes/youtube/youtube_channel_id"

# Move the working dir up one directory
import sys
sys.path.insert(0,'..')

import unittest

from API.classes.youtube.youtube_channel_id import youtube_channel_id


class test_youtube_channel_id(unittest.TestCase):
    def setUp(self):

        # This list contains a list of dicts with youtube URL's and thier
        # corresponding channel ID's
        self.channels = [
            {'url':'https://www.youtube.com/RandallsRelaxation',  'channel_id':'UCYCmal9NJFAJqPzJXkPkcpQ'}, # Shortened URL
            {'url':'www.youtube.com/RandallsRelaxation',          'channel_id':'UCYCmal9NJFAJqPzJXkPkcpQ'}, # Shortened URL without https://
            {'url':'youtube.com/RandallsRelaxation',              'channel_id':'UCYCmal9NJFAJqPzJXkPkcpQ'}, # Shortened URL without https://www.
            {'url':'https://www.youtube.com/c/News4JAX',          'channel_id':'UC_YFbvKedjnVjqrZqBR4L8Q'}, # /c/ URL
            {'url':'https://www.youtube.com/user/aragusea',       'channel_id':'UC9_p50tH3WmMslWRWKnM7dQ'}, # /user/ URL
            {'url':'https://www.youtube.com/channel/UCSnqXeK94-iNmwqGO__eJ5g',  'channel_id':'UCSnqXeK94-iNmwqGO__eJ5g'}, # /channel/ URL
            {'url':'https://www.youtube.com/channel/UCSnqXeK94-iNmwqGO__eJ5g',  'channel_id':'UCSnqXeK94-iNmwqGO__eJ5g'}, # /channel/ URL
            {'url':'youtube.com/KárolyZsolnai',                   'channel_id':'UCbfYPyITQ-7l4upoX8nvctg'}, # shortened URL with unqiue character
            {'url':'youtube.com/c/KárolyZsolnai',                 'channel_id':'UCbfYPyITQ-7l4upoX8nvctg'}, # /c/ URL with unqiue character
            {'url':'youtube.com/channel/UCbfYPyITQ-7l4upoX8nvctg','channel_id':'UCbfYPyITQ-7l4upoX8nvctg'}, # /channel/ URL without https://www.
            {'url':'https://www.youtube.com/user/keeroyz',        'channel_id':'UCbfYPyITQ-7l4upoX8nvctg'}, # /user/ URL
            {'url':'https://www.google.com',                      'channel_id':None}, # An invalid URL
            {'url':'https://www.google.com/test.html',            'channel_id':None}, # An invalid URL
        ]

    def test_channels(self):
        # Use the youtube_channel_id class to convert the URL into a channel ID.
        # Compare the returned channel ID to the one stored in self.channels

        for channel in self.channels:
            returned_channel_id = youtube_channel_id().get_yt_channel_id(channel['url'])
            try:
                self.assertEqual(returned_channel_id, channel['channel_id'])
            except:
                print("Fail: " + str(channel['url']))
                self.assertEqual(returned_channel_id, channel['channel_id'])



if __name__ == '__main__':
    unittest.main()
