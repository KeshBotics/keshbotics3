# Author: @Travis-Owens
# Date: 2021-01-26
# Description: When an error is encountered the 'on_command_error' listener is
#               triggered and will relay the error information to the 'log_event' class.
#              The 'log_event' class is used to send events to the API via a POST request.
#               ('on_command_error' can be bypassed by calling 'log_event' directly)

import discord
from discord.ext import commands

import os
import traceback
import inspect
import requests
import json

class error_handling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Attempt to log events to API, if API is not reachable send message
        #  to defined discord channel.

        # Set the required variables for logging an event
        level = 30
        pathname = None
        class_name = "discord_async"
        function_name = str(ctx.command)
        exc_info = None
        message = str(error) + " channel:" + str(ctx.channel.id)

        # Log the event to the database via the API
        status = log_event(level, pathname, class_name, function_name, exc_info, message)

        if not status:
            # Adding log to database returned false (error)
            # Send message to defined channel
            critical_log_channel = self.bot.get_channel(int(os.getenv("DISCORD_LOG_CHANNEL_CRITICAL")))
            await critical_log_channel.send(str("Error logging discord_async error to API! | " + str(ctx.command) + " | " + str(error)))

        # Determine the error that occured and respond with an appropriate message.
        # Expected exceptions:
        #   - discord.errors.Forbidden: The bot lacks the required permissions
        #   - discord.ext.commands.MissingPermissions: The calling user lacks the required permissions to interact with the bot
        try:
            # Get the original error attributes
            error_attr = getattr(error, 'original', error)

            # Check if the error type matches discord.errors.Forbidden, this indicates that the bot lacks permissions.
            if isinstance(error_attr, discord.errors.Forbidden):
                # If this sends successfully, the bot lacks the permission to send embedded messages.
                # If this fails to send, the bot lacks permissions to send both embedded messages and plain-text messages.
                # Failure to send will trigger the discord.errors.Forbidden exception below.
                await ctx.send(content="Error! Unable to embed links in this channel! Please adjust the permissions so that I can embed links.")

            # Check if the error type matches discord discord.ext.commands.MissingPermissions
            elif isinstance(error_attr, discord.ext.commands.MissingPermissions):
                # The calling user is missing the required guild permisions to interact with the bot.
                # Interactions with this bot typically requires that the user has the "manage_messages" permission.
                await ctx.send(error_attr)

            else:
                # An unexpected error occured, send generic message indicating an error.
                await ctx.send('Error handling command! The development team has been notified.')

        except discord.errors.Forbidden:
            # Unable to send message in current channel, notify the calling user and guild owner via direct message.
            #  Calling user referes to the user who executed the command.
            error_msg = "I've encountered an error! \n Guild: ```" + str(ctx.guild.name) + "``` Channel: ```" + str(ctx.channel.name) + "```Please ensure that I'm able to read messages, send messages, and embed links in this channel."

            # Send a direct message to the calling user.
            calling_user = await self.bot.fetch_user(int(ctx.message.author.id))
            await calling_user.send(error_msg)

            # If the calling user is not the guild owner, send a direct message to the guild owner also.
            if(ctx.message.author.id != ctx.guild.owner.id):
                guild_owner = await self.bot.fetch_user(int(ctx.guild.owner.id))
                await guild_owner.send(error_msg)

        except Exception as e:
            # Unexpected Exception, attempt to log.
            # Create string with exception information
            message = str(e) + " " + str(type(e).__name__)

            # Attempt to log exception details to database via the API
            log_event(50, "error_handling.py", "error_handling", "on_command_error", None, message)

def setup(bot):
    bot.add_cog(error_handling(bot))


class log_event(object):
    def __new__(self, level, pathname, class_name, function_name, exc_info, message):
        # This function will create a POST request to the API

        headers = {'auth':os.getenv("API_AUTH_CODE")}

        data = { "log_level":level,
                 "log_pathname":pathname,
                 "log_class_name":class_name,
                 "log_function_name":function_name,
                 "log_exc_info":exc_info,
                 "log_message":message
            }

        res = requests.post(os.getenv("API_URL") + "/log", headers=headers, data=json.dumps(data))

        if(res.status_code != 200):
            # Error logging to database
            return(False)

        return(True)
