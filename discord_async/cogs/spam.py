
import discord
from discord.ext import commands

from time import sleep
import os

usage = '<@username> <times>'
usage_p = os.getenv("COMMAND_PREFIX") + ' ' + usage

class spam_cog(commands.Cog):

    def __init__(self, bot):
        # self.bot = bot
        return None

    @commands.command(usage=usage, description='The spam command')
    async def spam(self, ctx, username, times: int):
        # Don't spam me
        if(username == '221396056775196672'):
            await ctx.send("You may not spam my master!")
            return

        # Add in message for Alex
        if(username == '413878816356958209'):
            await ctx.send("Typical Jig")

        # Set's max messages to 10 (minimize spam)
        if(int(times) > 10):
            times = 10

        for i in range(0,times):
            await ctx.send(username)
            sleep(0.5) # # TODO: convert to async sleep

    # Can only have one instance of this?
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     await ctx.send('Usage: ```' + usage_p + '```')
    #     await ctx.send(error)

def setup(bot):
    bot.add_cog(spam_cog(bot))
