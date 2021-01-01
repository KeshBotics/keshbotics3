# Author: @Travis-Owens
# Date: 2020-12-15
# Description:
import falcon
import json

from classes.discord.discord_auth_token import discord_auth_token

class discord_auth_validate(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):

        validatation_status = discord_auth_token().validate_auth_code(req.headers['CODE'])

        data = {'validation':validatation_status}

        resp.status = falcon.HTTP_200

        # Prepare response data, in JSON format
        resp.content_type = ['application/json']
        resp_data = json.dumps(data)
        resp.body = resp_data
