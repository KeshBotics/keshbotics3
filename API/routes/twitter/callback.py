
import falcon
import json

class twitter_callback(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        data = json.loads(req.bounded_stream.read().decode())
        print(data)
