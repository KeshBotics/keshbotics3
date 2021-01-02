import discord
from discord.ext import commands

import requests
import json
import os

usage = '<action (add/del/delete)> <twitch_username>'
usage_p = os.getenv('COMMAND_PREFIX') + ' ' + usage

class twitch_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage=usage)
    async def twitch(self, ctx, *args):

        actions = ['add', 'del', 'delete']
        # usage   = 'Usage: ```' + command_prefix + 'twitch <action> <twitch username>``` \n Actions: ' + str(actions)

        if(len(args) in [0,1]):
            await ctx.send('Incorrect Arguments! \n ' + usage_p)
            return

        if args[0] not in actions:
            await ctx.send('Allowed Actions: ' + str(actions))
            return

        action          = str(args[0])
        twitch_username = str(args[1])
        discord_channel_id = str(ctx.channel.id)

        headers = {'auth':os.getenv('API_AUTH_CODE'), 'twitch-username':twitch_username, 'discord-channel-id': discord_channel_id}

        if(action == 'add'):
            resp = requests.get(str(os.getenv('API_URL') + "/twitch/manage/add"), headers=headers)
        elif(action in ['del', 'delete']):
            resp = requests.get(str(os.getenv('API_URL') + "/twitch/manage/delete"), headers=headers)

        data = json.loads(resp.content)

        if(data['message']):
            await ctx.send(data['message'])
        else:
            await ctx.send('Back-end server error!')

def setup(bot):
    bot.add_cog(twitch_cog(bot))
