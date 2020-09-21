import discord
from discord.ext import commands


class ping_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ping(self, ctx):
        print(ctx.message)
        await ctx.send('pong2')


def setup(bot):
    bot.add_cog(ping_cog(bot))
