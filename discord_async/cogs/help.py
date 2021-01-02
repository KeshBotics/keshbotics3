# Author: @Travis-Owens
# Date: 2021-01-01
# Description: This cog is used to provide guidance on usage of the bot.

import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx,  *args):

        commands = 

        # Display all available commands
        if len(args) is 0:
            await ctx.send("Default help menu")



        await ctx.send('Help Test')

def setup(bot):
    bot.add_cog(help_cog(bot))
