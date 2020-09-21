import discord
from discord.ext import commands

class guild_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guild(self, ctx, *args):
        for guild in self.bot.guilds:
            link =  await guild.text_channels[0].create_invite(max_age=3600)
            print(link)
            break


def setup(bot):
    bot.add_cog(guild_cog(bot))
