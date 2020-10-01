import discord
from discord.ext import commands

import os

purge_usage = os.getenv('COMMAND_PREFIX') + 'purge <number of messages>'
purge_description = "This command will purge the defined amount of recent messages from the current channel."

class purge_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="purge", usage=purge_usage, description=purge_description)
    async def purge(self, ctx, number_of_messages = None):
        if(number_of_messages == None):
            await ctx.send("Usage: ```" + purge_usage + "```")
            return

        try:
            int(number_of_messages)
        except:
            await ctx.send("Please select a number! \n Usage: ```" + purge_usage + "```")
            # await ctx.send(purge_usage)
            return

        if(int(number_of_messages) > 128 or int(number_of_messages) < 1):
            await ctx.send("Invalid number of messages. Please select a number between 0 and 128.")
            return

        messages = await ctx.channel.history(limit=int(number_of_messages)+1).flatten()

        messages.reverse()
        for i, message in enumerate(messages):
            await message.delete()

def setup(bot):
    bot.add_cog(purge_cog(bot))
