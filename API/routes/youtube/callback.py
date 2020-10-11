import falcon
import json
from bs4 import BeautifulSoup

# from classes.discord_post import discord_post
from classes.youtube.youtube import youtube

class youtube_callback(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        resp.status       = falcon.HTTP_200               # Set response type
        resp.content_type = ['application/json']          # Set content_type
        resp.body         = req.params['hub.challenge']   # Body of response

    def on_post(self, req, resp):
        # Read data from POST
        data = req.bounded_stream.read().decode('UTF-8')

        # Parse the data using BeautifulSoup and XML parser
        bs_data = BeautifulSoup(data,"xml")

        # Select out the relavent data
        # video_url    = bs_data.feed.entry.link['href']
        channel_id   = bs_data.feed.entry.findAll('yt:channelId')[0].contents[0]
        video_id     = bs_data.feed.entry.findAll('yt:videoId')[0].contents[0]
        video_author = bs_data.feed.entry.author.findAll('name')[0].contents[0]
        video_title  = bs_data.feed.entry.title.contents[0]

        youtube().post_notification(channel_id, video_id, video_author, video_title)
