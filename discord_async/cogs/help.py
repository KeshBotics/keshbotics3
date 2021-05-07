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

    @commands.command(usage=usage, description="Command Usage", hidden=True)
    async def help(self, ctx,  *args):
        # Creates a message detailing the usage of available commands.
        # This is created dynamically, however, requires that usage and description
        # variables are set for each command.

        embed = discord.Embed(title="KeshBotics Commands:", colour=discord.Colour(0xd06412))
        embed.set_author(name="KeshBotics", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/avatars/532575955324239882/653f3b3749c3da11947a70881d675160.png")

        # Create a dictionary of the available commands
        # This will allow for the order of commands in the help dialog to be static
        available_commands = dict()
        for command in self.bot.commands:
            available_commands[command.name] = command

        # List of commands to display in the help menu
        display_commands = ["twitch", "youtube", "list", "request"]

        # Loop over the display_commands list and attempt to add the command
        #  description and usage to the help menu dialog
        for command in display_commands:
            if command in available_commands:
                embed.add_field(name=available_commands[command].description, value=available_commands[command].usage, inline=False)
            else:
                print("Command: " + command + " is unavailable!")

        # # bot.commands returns a set of the loaded commands
        # for command in self.bot.commands:
        #     # Some commands are hidden (ie. cogs.owner)
        #     if command.hidden is False:
        #         embed.add_field(name=command.description, value=command.usage, inline=False)

        await ctx.send(content="", embed=embed)

def setup(bot):
    bot.add_cog(help_cog(bot))
