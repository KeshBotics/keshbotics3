# Author: @Travis Owens
# Date: 2020-02-20
# Description: This is the primary interface for interacting with the database.
#               The purpose of this class is to create a standardized/modular
#               method of accessing the database resources.

import pymysql
import os
from classes.event_logging.event_logging import get_logger

class data_handler(object):
    def __init__(self):

        self.defined_queries = {
            'discord_channels_by_twitch_user_id':'SELECT DISTINCT `discord_channel_id` FROM `twitch_notifications` WHERE `twitch_user_id`=%s',
            'unique_twitch_notification':'SELECT * FROM `twitch_notifications` WHERE `twitch_username` = %s  AND `discord_channel_id` = %s',
            'add_twitch_notification':'INSERT INTO `twitch` VALUES(null,%s,%s,%s,0)',
            'delete_twitch_notification':'DELETE FROM `twitch` WHERE `twitch_username`=%s AND `twitch_user_id`=%s AND `discord_channel_id`=%s',
            'is_streaming':'SELECT `streaming` FROM `twitch` WHERE `twitch_user_id`=%s LIMIT 1',
            'update_is_streaming':'UPDATE `twitch` SET `streaming` =  %s WHERE `twitch_user_id` = %s',
            'twitch_oauth_token':'SELECT `setting_value` FROM `settings` WHERE `setting_key` = "twitch_oauth_token"'
        }


    def get_connection(self):
        return(pymysql.connect(host=os.getenv('DB_HOST').strip("\r"),
                                     user=os.getenv('DB_USER').strip("\r"),
                                     password=os.getenv('DB_PASS').strip("\r"),
                                     db=os.getenv('DB_NAME').strip("\r"),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor))


    def defined_select(self, key, input, values_only=False):
        # key = dict key for query in self.defined_queries.
        # input = Values to insert into the defined query.
        # values_only = strip the values from the cursor.fetchall(),
        #   ex: list of discord_channel_ids; instead of list of dicts

        conn = self.get_connection()

        with conn.cursor() as cursor:
            cursor.execute(self.defined_queries[key], input)

        if(values_only == True):
            data = cursor.fetchall()
            return(list(map(lambda x : x['discord_channel_id'], data)))

        return(cursor.fetchall())

    def defined_insert(self, key, input):

        try:
            conn = self.get_connection()

            with conn.cursor() as cursor:
                cursor.execute(self.defined_queries[key], input)

            conn.commit()
            conn.close()

            return(True)

        except Exception as e:
            get_logger().error(e, exc_info=True)
            return(False)

    def defined_delete(self, key, input):

        try:
            conn = self.get_connection()

            with conn.cursor() as cursor:
                cursor.execute(self.defined_queries[key], input)

            conn.commit()
            conn.close()

            return(True)

        except Exception as e:
            get_logger().error(e, exc_info=True)
            return(False)

    def defined_update(self, key, input):

        try:
            conn = self.get_connection()

            with conn.cursor() as cursor:
                cursor.execute(self.defined_queries[key], input)

            conn.commit()
            conn.close()

            return(True)

        except Exception as e:
            get_logger().error(e, exc_info=True)
            return(False)

    def select(self, sql, input, values_only=False):
        try:
            conn = self.get_connection()

            with conn.cursor() as cursor:
                cursor.execute(sql, input)

            return(cursor.fetchall())

        except Exception as e:
            get_logger().error(e, exc_info=True)

    def insert(self, sql, input):

        try:
            conn = self.get_connection()

            with conn.cursor() as cursor:
                cursor.execute(sql, input)

            conn.commit()
            conn.close()

            return(True)

        except Exception as e:
            get_logger().error(e, exc_info=True)
            return(False)

    def update(self, sql, input):

        try:
            conn = self.get_connection()

            with conn.cursor() as cursor:
                cursor.execute(sql, input)

            conn.commit()
            conn.close()

            return(True)
        except Exception as e:
            get_logger().error(e, exc_info=True)
            return(False)

    def delete(self, sql, input):

        try:
            conn = self.get_connection()

            with conn.cursor() as cursor:
                cursor.execute(sql, input)

            conn.commit()
            conn.close()

            return(True)
        except Exception as e:
            get_logger().error(e, exc_info=True)
            return(False)
