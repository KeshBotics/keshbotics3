import discord
from discord.ext import commands


class error_handling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This is very basic handling of command errors
        await ctx.send(error)


def setup(bot):
    bot.add_cog(error_handling(bot))
