import falcon
import json
from bs4 import BeautifulSoup

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
        video_title  = bs.feed.entry.title.contents[0]
        video_author = bs.feed.entry.author.findAll('name')[0].contents[0]
        video_url    = bs.feed.entry.link['href']

        

        # print("Video Titled: " + video_title)
        # print("Uploaded By: " + video_author)
        # print("Link: " + video_url)
