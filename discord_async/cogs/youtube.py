import discord
from discord.ext import commands

import requests
import json
import os

usage = os.getenv('COMMAND_PREFIX') + '<action (add/del/delete)> <YouTube channel URL>'

class youtube_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage=usage, description="YouTube Notifications")
    async def youtube(self, ctx, *args):

        actions = ['add', 'del', 'delete']

        if(len(args) in [0,1]):
            await ctx.send('Incorrect Arguments! \n ' + usage)
            return

        if args[0] not in actions:
            await ctx.send('Allowed Actions: ' + str(actions))
            return

        action              = str(args[0])
        youtube_channel_url = str(args[1])
        discord_channel_id  = str(ctx.channel.id)

        headers = {'auth':os.getenv('API_AUTH_CODE').strip("\r"), 'youtube-channel-url':youtube_channel_url, 'discord-channel-id': discord_channel_id}

        if(action == 'add'):
            resp = requests.get(str(os.getenv('API_URL').strip("\r") + "/youtube/manage/add"), headers=headers)
        elif(action in ['del', 'delete']):
            resp = requests.get(str(os.getenv('API_URL').strip("\r") + "/youtube/manage/delete"), headers=headers)

        data = json.loads(resp.content)

        if(data['message']):
            await ctx.send(data['message'])
        else:
            await ctx.send('Back-end server error!')


def setup(bot):
    bot.add_cog(youtube_cog(bot))
