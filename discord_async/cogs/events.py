# Author: @Travis-Owens
# Date: 2021-01-17
# Desc: This cog uses the "discord.on_guild_channel_delete"  and
#         "discord.on_guild_remove" events to detect channel/guild deletions.
#          A request is made to the API to delete notifications associated with
#          either the Discord Guild ID or the Discord Channel ID


import discord
import os
import requests

from discord.ext import commands

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        r = requests.delete(url=str(os.getenv("API_URL") + "/notifications"), headers={'auth':os.getenv("API_AUTH_CODE"), 'discord-guild-id':str(guild.id)})

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        r = requests.delete(url=str(os.getenv("API_URL") + "/notifications"), headers={'auth':os.getenv("API_AUTH_CODE"), 'discord-channel-id':str(channel.id)})

def setup(bot):
    bot.add_cog(events(bot))
