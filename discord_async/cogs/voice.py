import discord
from discord.ext import commands

# import PyNaCl


class voice_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *args):
        channel = ctx.author.voice.channel
        await channel.connect()


    @commands.command()
    async def leave(self, ctx, *args):
        await ctx.voice_client.disconnect()

def setup(bot):
    bot.add_cog(voice_cog(bot))
