# Author: @Travis-Owens
# Date: 2021-01-12
# Desc: This command is used to retrieve a list of notifications on a per
#       discord channel basis

import discord
from discord.ext import commands

import requests
import json
import os

usage = os.getenv('COMMAND_PREFIX') + 'list <platform (Twitch/YouTube)>'

class notification_list_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage=usage, description="Notification List", aliases=['notifications'])
    @commands.has_permissions(manage_messages=True)
    async def list(self, ctx, platform = None):
        # NOTE: if platform is not provided (None), return notifications for all platforms

        # Define supported platforms
        platforms = ['twitch', 'youtube']
        if(platform is not None and platform.lower() not in platforms):
            # If provided platform doesn't exist, revert to displaying all notifications
            platform = None

        # Route requires, headers auth and discord-channel-id
        headers = {
                    'auth': os.getenv('API_AUTH_CODE').strip("\r"),
                    'discord-channel-id': str(ctx.channel.id)
                }

        # Query notifications route of the API
        resp = requests.get(str(os.getenv('API_URL').strip("\r") + '/notifications'), headers = headers)

        # Ensure proper status code
        if(resp.status_code != 200):
            # Expected status code is 200
            await ctx.send('Back-end server error!')
            return

        # Convert the JSON response to a python dictionary
        data = json.loads(resp.content)

        # Create embeded message
        embed = discord.Embed(colour=discord.Colour(0xd06412))
        embed.set_author(name="KeshBotics Notifications", url="", icon_url="https://cdn.discordapp.com/avatars/532575955324239882/653f3b3749c3da11947a70881d675160.png")

        # Add field for Twitch Notifications
        if(platform is None or platform.lower() == 'twitch' ):
            embed.add_field(name="Twitch", value=notification_strings().get_twitch_str(data[str(ctx.channel.id)]['twitch']), inline=False)

        # Add field for YouTube Notifications
        if(platform is None or platform.lower() == 'youtube' ):
            embed.add_field(name="YouTube", value=notification_strings().get_youtube_str(data[str(ctx.channel.id)]['youtube']), inline=False)

        await ctx.send(content="", embed=embed)

class notification_strings(object):
    def __init__(self):
        pass

    def get_twitch_str(self, twitch_channels):
        # Creates a list in string format
        # Adds hyperlinks to the twitch_username (markup)

        if twitch_channels is None:
            return('No Twitch notifications found.\n\n')

        twitch_str = ''
        for channel in twitch_channels:
            twitch_str += str("[" + channel['twitch_username'] + "](https://twitch.tv/" + channel['twitch_username'] + ")\n")

        twitch_str += "Remove a Twitch notification: ```k!twitch del <twitch_username>```\n"
        twitch_str += "\n\n\n"

        return(twitch_str)

    def get_youtube_str(self, youtube_channels):
        # Creates a list in string format

        if youtube_channels is None:
            return('No YouTube notifications found.\n\n')

        youtube_str = ''
        for channel in youtube_channels:
            youtube_str += str("[" + channel["youtube_display_name"] + "](https://youtube.com/channel/" + channel['youtube_channel_id'] + ")\n")

        youtube_str += "Remove a YouTube notification: ```k!youtube del <YouTube channel URL>```\n"
        youtube_str += "\n\n"

        return(youtube_str)

def setup(bot):
    bot.add_cog(notification_list_cog(bot))
