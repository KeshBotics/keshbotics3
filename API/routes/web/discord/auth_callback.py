# Author: @Travis-Owens
# Date: 2020-12-15
# Description:
import falcon
import json

from classes.discord.discord_auth_token import discord_auth_token

class discord_auth_callback(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        # This is used during the web authentication flow,
        # Using the discord_auth_token class use the generated authorization_code
        #   to retrieve a auth_token from discord

        data = req.bounded_stream.read().decode('UTF-8')

        discord_auth_obj = discord_auth_token()

        # Check if "CODE" is sent in the headers
        # if it's not included trigger a 401 return
        # if it is included, attempt to retrieve the auth token from discord
        if req.headers['CODE'] is None:
            # "CODE" is not included in the headers
            auth_resp = {'success':False}
        else:
            auth_resp = discord_auth_obj.get_token(req.headers['CODE'])

        # If token retrieval was successful, return 200 else return 401
        if(auth_resp['success'] == True):
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

        # Prepare response data, in JSON format
        resp.content_type = ['application/json']
        resp_data = json.dumps(auth_resp)
        resp.body = resp_data


    def on_post(self, req, resp):
        print(req.headers)
        data = req.bounded_stream.read().decode('UTF-8')
        print(data)
