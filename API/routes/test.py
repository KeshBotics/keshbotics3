# Description: This route is used to test the general availability of the API.

import falcon

class test(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200               # Set response type
        resp.content_type = ['application/json']    # Set content_type
        resp.body = "Test successful"               # Set response body

    def on_post(self, req, resp):
        pass
