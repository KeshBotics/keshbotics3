import discord
from discord.ext import commands

import os

purge_usage = os.getenv('COMMAND_PREFIX') + 'purge <number of messages>'
purge_description = "This command will purge the defined amount of recent messages from the current channel. The permission 'manage_messages' is required."

class purge_cog(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot


    @commands.command(name="purge", usage=purge_usage, description=purge_description)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number_of_messages = None):

        # Check if number_of_messages is an(can be) and int, if not send usage instructions
        try:
            int(number_of_messages)
        except:
            await ctx.send("Please select a number! \n Usage: ```" + purge_usage + "```")
            return

        # Set lower and upper limits for message purging (1-128)
        if(int(number_of_messages) > 128 or int(number_of_messages) < 1):
            await ctx.send("Invalid number of messages. Please select a number between 0 and 128.")
            return

        # Retrieve the defined amount of recent messages
        # Add 1 to account for the message used to execute this command (k!purge x)
        messages = await ctx.channel.history(limit=int(number_of_messages)+1).flatten()

        # This will make the purging flow better visually
        messages.reverse()

        # iterate over the messages and delete each
        for i, message in enumerate(messages):
            await message.delete()

def setup(bot):
    bot.add_cog(purge_cog(bot))
