import discord
from discord.ext import commands

usage = os.getenv('COMMAND_PREFIX') + 'ping'
class ping_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage=usage, description="Ping KeshBotics")
    async def ping(self, ctx):
        await ctx.send('pong')

def setup(bot):
    bot.add_cog(ping_cog(bot))
