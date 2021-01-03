# Author: @Travis-Owens
# Date: 2021-01-01
# Description: This cog is used to provide guidance on usage of the bot.

import discord
from discord.ext import commands
import os

usage = os.getenv('COMMAND_PREFIX') + 'help'

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage=usage, description="Command Usage")
    async def help(self, ctx,  *args):
        # Creates a message detailing the usage of available commands.
        # This is created dynamically, however, requires that usage and description
        # variables are set for each command.

        default_help_message = "```"

        # bot.commands returns a set of the loaded commands
        for command in self.bot.commands:
            # Some commands are hidden (ie. cogs.owner)
            if command.hidden is False:
                default_help_message += f"{command.description}: {command.usage}\n"

        default_help_message += "```"

        await ctx.send(default_help_message)

def setup(bot):
    bot.add_cog(help_cog(bot))
