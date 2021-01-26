# Author: @Travis-Owens
# Date: 2021-01-20
# Desc: This class is used to log events to the database with a redundancy of
#        sending a Discord message via HTTP. Due to storage limitations of docker
#        errors are not logged to a local file. In the event that the database and
#        discord are both unreachable, events will only be displayed in the console.

import logging
import inspect
import os
import pymysql
import requests
import json

class event_log(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def get_connection(self):
        return(pymysql.connect(host=os.getenv('DB_HOST').strip("\r"),
                                     user=os.getenv('DB_USER').strip("\r"),
                                     password=os.getenv('DB_PASS').strip("\r"),
                                     db=os.getenv('DB_NAME').strip("\r"),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor))

    def emit(self, record):
        # This function is triggered when an event occurs
        # Attempts to log events to both the databse and Discord

        # Ensure that record.msg is a string, (this could be an exception object)
        record.msg = str(record.msg)

        # Selects the calling class and function name from the stack, add the string
        #  values to the record object
        # NOTE: This may not be a reliable method of getting the class and function names
        try:
            record.class_name, record.func_name = inspect.stack()[7][4][0].strip("\n").split(".")
        except:
            record.class_name, record.func_name = None, record.funcName

        # Insert the record into the database, if successful returns True, else False
        db_status = self.db_insert_record(record)

        # Post the record to Discord, if successful returns True, else False
        discord_status = self.discord_post_record(record)

        if not db_status:
            # Inserting the log into the database failed, send an alert via discord
            self.discord_post_log(50, "Logging to Database Failed!")

        if not discord_status:
            # Posting the log to Discord failed, send an alert to the database
            self.db_insert_log(50, 'db_log.py' ,'db_log', 'emit', None, 'Discord post Failed')

        if not db_status and not discord_status:
            # This could be the result of a misconfigured environment variable file
            print("CRITICAL ERROR: Niether the database nor Discord are reachable!")
            print("Failed to Log: " + str(record.class_name) + "." + str(record.func_name) + ": " + str(record.msg))

    def db_insert_record(self, record):
        # Helper function
        # Prepares the information in the record object to be inserted into the DB
        #  and uses db_insert_log() to insert into the database

        try:
            return(self.db_insert_log(record.levelno, record.pathname, record.class_name, record.func_name, record.exc_info, record.msg))
        except Exception as e:
            print("DB_LOG: Exception while parsing record object (DB): " + str(e))
            return(False)

    def db_insert_log(self, level, pathname, class_name, function_name, exc_info, message):
        # This can be called directly in the event a record object is not created
        # Return True indicates success, returning False indicates failure

        try:
            # Create query to insert values into the `logging` table
            # Required columns are: level, class_name, function_name, and message
            sql    = "INSERT INTO `logging` VALUES(NULL, NULL, %s, %s, %s, %s, %s, %s)"
            values = [level, pathname, class_name, function_name, str(exc_info), message]

            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, values)

            # If inserting into the database, commit() will trigger an exception.
            conn.commit()
            conn.close()

            return(True)

        except Exception as e:
            print("DB_LOG: Exception while inserting to DB: " + str(e))
            return(False)

    def discord_post_record(self, record):
        # Helper function
        # Formats the information from the record object into a string and uses
        #  discord_post_msg() to post the message to Discord

        try:
            message = str(record.levelname) + " | " + str(record.pathname) + " | " + str(record.class_name) + " | " + str(record.func_name) + " | " + str(record.exc_info) + " | " + str(record.msg)
            return(self.discord_post_log(record.levelno, message))

        except Exception as e:
            print("DB_LOG: Exception while parsing record object (Discord): " + str(e))
            return(False)

    def discord_post_log(self, log_level, message):
        # This can be called directly in the event a record object is not created
        # Post a message to Discord via HTTP

        # NOTE: This function can add between .2 and .3 seconds to the execution time
        #           (depends on network latency).
        #       The env variable "DISCORD_MIN_TO_LOG" is used to eliminate some of this latency in production.
        #           Typically, this variable is used avoid posting INFO and DEBUG events.
        #       This does not have an effect on database logging.

        try:
            if(log_level < int(os.getenv("DISCORD_MIN_TO_LOG"))):
                # Log level is below the threshold to be logged to Discord
                return(True)

            # Retrieve the appropriate Discord channel ID
            discord_channel_id = self.discord_get_channel_id(log_level)

            headers = { "Authorization":"Bot {}".format(os.getenv('DISCORD_BOT_TOKEN').strip("\r")),
                            "User-Agent":"KeshBotics (v3.3)",
                            "Content-Type":"application/json", }

            message = json.dumps({"content":message})

            discord_message_url = "https://discordapp.com/api/channels/{}/messages".format(discord_channel_id)
            r = requests.post(discord_message_url, headers = headers, data =message)

            if r.status_code != 200:
                raise Exception("Discord HTTP status code", r.status_code)

            return(True)

        except Exception as e:
            print("DB_LOG: Exception while posting to Discord: " + str(e))
            return(False)


    def discord_get_channel_id(self, log_level):
        # Helper function for discord_post_log()
        # Converts the log level to the appropriate Discord channel id

        if(log_level >= 50):
            return(os.getenv("DISCORD_LOG_CHANNEL_CRITICAL"))
        elif(log_level >= 40):
            return(os.getenv("DISCORD_LOG_CHANNEL_ERROR"))
        elif(log_level >= 30):
            return(os.getenv("DISCORD_LOG_CHANNEL_WARNING"))
        elif(log_level >= 20):
            return(os.getenv("DISCORD_LOG_CHANNEL_INFO"))
        elif(log_level >= 10):
            return(os.getenv("DISCORD_LOG_CHANNEL_DEBUG"))

        return(os.getenv("DISCORD_LOG_CHANNEL_NOTSET"))

class get_logger(object):
    def __new__(cls, name = None):
        # Helper function for creating a logging object
        if name is None:
            # Get __name__ of caller from the stack
            frm  = inspect.stack()[1]
            name = inspect.getmodule(frm[0]).__name__

        log = logging.getLogger(name)

        if not log.hasHandlers():
            # If the logger does not have handlers, init them now.
            # This prevents log/handler duplication
            log.setLevel(logging.DEBUG)
            log.addHandler(event_log())
            log.propagate = False

        return(log)
