# Author: @Travis-Owens
# Date: 2021-03-11
# Description: This cog is used to manage notification override limits (bot owner only)
#  This also contains a command for discord guilds to request an notification limit increase.

import discord
from discord.ext import commands

import requests
import json
import os

request_usage = os.getenv('COMMAND_PREFIX') + 'request'

class notification_limits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage=request_usage, description="Request notification limit increase")
    @commands.has_permissions(manage_messages=True)
    async def request(self, ctx):
        # This cog will send an alert to the developers.
        # Send message to the info channel
        info_log_channel = self.bot.get_channel(int(os.getenv("DISCORD_LOG_CHANNEL_INFO")))
        await info_log_channel.send(str("Request for notification limit increase: \nGuild ID: " + str(ctx.guild.id) + "\nGuild Name: " + str(ctx.guild.name) + "\nMember Count: " + str(ctx.guild.member_count)))

        await ctx.send(content="The developement team has been notified of the notification limit increase request. Please allow 48 hours for the devs to review the request.")

    @commands.command(name='override', hidden=True)
    @commands.is_owner()
    async def override(self, ctx, action = None, discord_guild_id = None, platform = None, override = None):

        # Define the allowed actions
        allowed_actions = ['check', 'set', 'delete']
        # ensure that the action is a lowercase string
        action = str(action).lower()

        # Set the header values
        headers = {'auth':os.getenv('API_AUTH_CODE'),
                   'discord-guild-id':str(discord_guild_id),
                   'platform':str(platform),
                   'override':str(override)
                }

        if action in ["check", "get"]:
            # Get the notification limit
            r = requests.get(url=str(os.getenv('API_URL') + "/notifications/limits"), headers=headers)

        elif action in ["set", "update"]:
            # Set the notification limit
            r = requests.put(url=str(os.getenv('API_URL') + "/notifications/limits"), headers=headers)

        elif(action == "delete"):
            # Delete the notification limit
            r = requests.delete(url=str(os.getenv('API_URL') + "/notifications/limits"), headers=headers)

        else:
            await ctx.send('Allowed Actions: ' + str(allowed_actions))
            return

        await ctx.send(content=str(json.loads(r.content.decode('utf-8'))))

def setup(bot):
    bot.add_cog(notification_limits(bot))
