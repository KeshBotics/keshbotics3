# Author: @Travis-Owens
# Date:  2020-02-16
# Description: Used for authenticated routes

import falcon
import json
import os

class auth(object):
    def __init__(self):
        pass

    def __call__(self, req, resp, resource, params):
        # Checks if the auth header matches the valid api_auth_code
        auth_code = req.get_header('auth')

        if(auth_code != os.getenv('API_AUTH_CODE').strip("\r")):
            raise falcon.HTTPUnauthorized('Authentication Required', 'Provide authentication code in auth header.')
