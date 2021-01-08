# Author: @Travis-Owens
# Date: 2021-01-01
# Description: This cog is currently being "reimagined", and is not available in production.
#               

import discord
from discord.ext import commands

import json
import requests
import datetime
import os

usage = 'history <twitch_username>'
usage_p = os.getenv('COMMAND_PREFIX') + ' ' + usage
description = 'Notice: This command only works for channels tracked by Keshbotics!'

class twitch_history_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='history', usage=usage, description=description)
    async def twitch_history(self, ctx, twitch_username=None):

        if twitch_username is None:
            # Displays the proper usages of the command
            await ctx.send(usage_p)
            return

        resp = requests.get(str(os.getenv('API_URL') + "/twitch/metrics/" + twitch_username))

        data = json.loads(resp.content)

        message = 'Time Metrics for the Last 10 Streams \nDate - - - - - Stream Length\n'

        for stream in data['streams']:
            date = datetime.datetime.strptime(stream['stream_start'], '%Y-%m-%d %H:%M:%S')
            row = str(date.year) + '/' + str(date.month) + '/' + str(date.day) + '    ' + stream['time'] + '\n'
            message += row

        message += '---------------------------------\n'
        message += 'Total:          ' + data['total'] + '\n'

        total       = datetime.datetime.strptime(data['total'], '%H:%M:%S')
        total_delta = datetime.timedelta(hours=total.hour,minutes=total.minute, seconds=total.second)
        message     += 'Average:    ' + str(total_delta/len(data['streams']))

        await ctx.send(message)


def setup(bot):
    bot.add_cog(twitch_history_cog(bot))
