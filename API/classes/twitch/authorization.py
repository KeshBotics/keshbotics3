# Author: @Travis-Owens
# Date: 2020-05-07
# Desc: for some reason, twitch thinks oauth2 is necessiary for accessing publicly
# available data.

# import requests
#
# # import config
#
# class twitch_authorization(object):
#     def __init__(self):
#         self.twitch_id_url = 'https://id.twitch.tv/oauth2/token'
#
#     def get_token(self, with_token_type = True):
#
#         params = {
#             'client_id': config.TWITCH_CLIENT_ID,
#             'client_secret': config.TWITCH_SECRET,
#             'grant_type': 'client_credentials'
#         }
#
#         resp = requests.post(self.twitch_id_url, params=params)
#
#         data = resp.json()
#
#         if(with_token_type):
#             return(str(data['token_type'] + ' ' + data['access_token']))
#
#         return(data['access_token'])
#

# x = twitch_authorization().get_token()
# print(x)
