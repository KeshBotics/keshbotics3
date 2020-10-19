# Author: @Travis-Owens
# Date: 2020-01-24
# Description: Public facing API portion of Keshbotics. Used to facilitate
#               communication between Twitch, YouTube, and Discord.

import falcon
import os

# middleware
from middleware.request_logging import request_logging
from middleware.print_x_real_ip import print_x_real_ip

# routes
from routes.root            import root
from routes.test            import test

# Twitch API routes
from routes.twitch.add      import twitch_add
from routes.twitch.delete   import twitch_delete
from routes.twitch.callback import twitch_callback
import routes.twitch.metrics as metrics

# YouTube API routes
from routes.youtube.callback import youtube_callback
from routes.youtube.add      import youtube_add
from routes.youtube.delete   import youtube_delete

class public_facing_api(object):
    def __init__(self):
        # The initialize function will define the API middleware and routes, and
        # create a falcon API object (self.app).

        # A list of middleware classes to execute before each request
        self.middleware = [request_logging()]

        # A list of the available API routes. Denoted by the path to the route and
        # the class that the route is associated with.
        self.routes = [
            {'route':'/twitch/manage/add',                  'class': twitch_add()},
            {'route':'/twitch/manage/delete',               'class': twitch_delete()},
            {'route':'/twitch/callback',                    'class': twitch_callback()},
            {'route':'/twitch/callback/{twitch_user_id}',   'class': twitch_callback()},
            {'route':'/twitch/metrics/{twitch_username}',   'class': metrics.twitch_metrics_username()},
            {'route':'/twitch/metrics/id/{twitch_user_id}', 'class': metrics.twitch_metrics_id()},

            {'route':'/youtube/callback',       'class': youtube_callback()},
            {'route':'/youtube/manage/add',     'class': youtube_add()},
            {'route':'/youtube/manage/delete',  'class': youtube_delete()},

            {'route':'/',       'class':root()}
            {'route':'/test',   'class': test()},
        ]

        # Create a falcon API object with defined middleware.
        self.app = falcon.API(middleware=self.middleware)

        # Add the API routes (self.routes) to the falcon API object.
        self.setup_routes()

    def setup_routes(self):
        # Add each route defined in self.routes to the falcon API object.
        for route in self.routes:
            self.app.add_route(route['route'], route['class'])

    def start(self):
        # Used for testing locally

        # simple_server should only be used when testing the API locally.
        from wsgiref import simple_server

        # If API_PORT is set as a system variable use it, else use 8445
        if(os.getenv('API_PORT') == None):
            port = 8445
        else:
            port = int(os.getenv('API_PORT'))

        # create a simple_server object to serve the API
        self.httpd = simple_server.make_server('0.0.0.0', port, self.app)
        self.httpd.serve_forever()

    def get_app(self):
        # Getter function for the falcon API object.
        return(self.app)


if __name__ == '__main__':
    # If the main.py is executed directly, the API will launch in "test" mode
    public_facing_api().start()
else:
    # Guincorn will look for the variable "app"
    app = public_facing_api().get_app()
