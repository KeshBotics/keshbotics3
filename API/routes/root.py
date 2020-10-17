# Description: This route is used to prevent the "/" API route from
#              returning a 404 or 500 http error.


import falcon

class root(object):
        def __init__(self):
            pass

        def on_get(self, req, resp):
            pass

        def on_post(self, req, resp):
            pass
