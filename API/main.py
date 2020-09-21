# Author: @Travis-Owens
# Date: 2020-01-24
# Description: General public facing API. Twitch, discord, etc

import falcon
import json
from wsgiref import simple_server
import os

# middleware
from middleware.request_logging import request_logging
from middleware.print_x_real_ip import print_x_real_ip

# routes
from routes.twitch.add      import twitch_add
from routes.twitch.delete   import twitch_delete
from routes.twitch.callback import twitch_callback
import routes.twitch.metrics as metrics

class public_facing_api(object):
    def __init__(self):

        self.middleware = [
            {'class': print_x_real_ip()}
        ]

        self.routes = [
            {'route':'/test',                   'class': test()},
            {'route':'/twitch/manage/add',      'class': twitch_add()},
            {'route':'/twitch/manage/delete',   'class': twitch_delete()},
            {'route':'/twitch/callback', 'class': twitch_callback()},
            {'route':'/twitch/callback/{twitch_user_id}', 'class': twitch_callback()},
            {'route':'/twitch/metrics/{twitch_username}', 'class': metrics.twitch_metrics_username()},
            {'route':'/twitch/metrics/id/{twitch_user_id}', 'class': metrics.twitch_metrics_id()},
            {'route':'/', 'class':root()}

        ]

        self.app = falcon.API(middleware=[request_logging(), print_x_real_ip()])
        self.setup_routes()
        # self.start()

    def setup_middleware(self):
        for middleware in self.middleware:
            self.app.add_middleware(middleware['class'])

    def setup_routes(self):
        for route in self.routes:
            self.app.add_route(route['route'], route['class'])

    def start(self):
        # Used for testing locally
        self.httpd = simple_server.make_server('0.0.0.0', int(os.getenv('API_PORT')), self.app)
        self.httpd.serve_forever()

    def get_app(self):
        return(self.app)

class test(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        print(req.get_header('x-real-ip'))
        print(req.headers)
        resp.status = falcon.HTTP_200   # Set response type
        resp.content_type = ['application/json']    # Set content_type
        resp.body = os.getenv('TEST_VAR')

    def on_post(self, req, resp):
        pass

class root(object):
        def __init__(self):
            pass

        def on_get(self, req, resp):
            pass

        def on_post(self, req, resp):
            pass


if __name__ == '__main__':
    public_facing_api().start()
else:
    app = public_facing_api().get_app()
