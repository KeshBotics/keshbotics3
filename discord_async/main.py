# Author: @Travis-Owens
# Date: 2020-02-16
# Description: Discord interface for general bot functionality

import discord
from discord.ext import commands
intents = discord.Intents(messages=True, guilds=True, members=True)


import os

# Create a bot object using the prefix definding the env file
bot = commands.Bot(command_prefix=os.getenv('COMMAND_PREFIX').strip("\r"), intents=intents)
# Remove the default help command
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    activity = discord.Game(name="k!help")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_message(message):
    # Can add things to do before processing command
    await bot.process_commands(message)

# Create a list of cogs
extensions = [  'cogs.owner',
                'cogs.twitch',
                'cogs.youtube',
                'cogs.error_handling',
                'cogs.help',
                'cogs.list',
                'cogs.events',
                'cogs.notification_limits'
                ]

# Load the cogs
for extension in extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(e)

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
