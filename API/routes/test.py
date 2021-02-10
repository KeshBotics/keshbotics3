# Description: This route is used to test the general availability of the API.

import falcon
from classes.event_logging.event_logging import get_logger


class test(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        # try:
        #     raise KeyError
        #
        #     resp.status = falcon.HTTP_200               # Set response type
        #     resp.content_type = ['application/json']    # Set content_type
        #     resp.body = "Test successful"               # Set response body
        # except Exception as e:
        #     get_logger().error(e, exc_info=True)
        resp.status = falcon.HTTP_200               # Set response type
        resp.content_type = ['application/json']    # Set content_type
        resp.body = "Test successful"               # Set response body

    def on_post(self, req, resp):
        pass
