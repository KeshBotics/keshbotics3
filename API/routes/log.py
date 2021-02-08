# Author: @Travis-Owens
# Date: 2021-01-26
# Description: This route is used to interact with the event_log class via the API.
#      on_get  - Will return a JSON object with x amount of recent events (with min-log-level selector available)
#      on_post - Will insert a new log event into the database

import falcon
import json
from classes.event_logging.event_logging import event_log, get_logger
from classes.data_handler import data_handler
from middleware.auth import auth

@falcon.before(auth())
class route_log(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        # Return a list of recent event entries.

        try:
            # Get level and limit variables from the headers
            # If the 'level' header is not provided, set it to 0
            if req.get_header('min-log-level') is None:
                level = 0
            else:
                # Will raise exception if cannot convert to int
                level = int(req.get_header('min-log-level'))

            # Create a soft limit of 100 events, this will prevent an excessive amount
            # of entries being returned. Also if limit is not provided, set it to 100
            if req.get_header('limit') is None:
                limit = 100
            else:
                # Get int value of limit, if limit is greater than 100: set to 100
                # Will raise exception if cannot convert to int
                limit = int(req.get_header('limit'))
                if limit > 100: limit = 100

            # Retrieve the requested entries from the database
            events = data_handler().select("SELECT * FROM `logging` WHERE `level` >= %s ORDER BY `id` DESC LIMIT %s", [level, limit])

            resp.status = falcon.HTTP_200
            resp.content_type = ['application/json']
            # default=str resloves an issue with datetime.datetime not being
            #    JSON serializable
            resp.body = json.dumps(events, default=str)

        except (TypeError, ValueError) as e:
            # Intended to capture value/type errors with header value int casting
            get_logger().warning(e, exc_info=True)

            resp.status = falcon.HTTP_400
            resp.content_type = ['application/json']
            resp.body = json.dumps({"status":"error", "code":400, "message":"Ensure that header values 'min-log-level' and 'limit' are integers."})

        except Exception as e:
            get_logger().error(e, exc_info=True)

            resp.status = falcon.HTTP_400
            resp.content_type = ['application/json']
            resp.body = json.dumps({"status":"error", "code":400, "message":"Failed to retrieve entries."})

    def on_post(self, req, resp):
        # Create a new log entry, this function will manually trigger the
        # 'db_insert_log' and 'discord_post_log' functions.
        try:
            # Create an event_log object, this provides access to DB and Discord functions
            log = event_log()

            # Expects data to be in JSON format in POST data
            data = json.loads(req.bounded_stream.read().decode('UTF-8'))

            # Insert a log entry into the database.
            db_status = log.db_insert_log(
                            data['log_level'],
                            data['log_pathname'],
                            data['log_class_name'],
                            data['log_function_name'],
                            data['log_exc_info'],
                            data['log_message']
                    )

            # If inserting the log into the database resulted in an error db_status = (false)
            if not db_status: raise

            # Send message to Discord, note: level must meet DISCORD_MIN_TO_LOG
            message = str(data['log_level']) + " | " + str(data['log_pathname']) + " | " + str(data['log_class_name']) + " | " + str(data['log_function_name']) + " | " + str(data['log_exc_info']) + " | " + str(data['log_message'])
            log.discord_post_log(int(data['log_level']), message)

            # Inserting entry was successful, return http_200 success
            resp.status = falcon.HTTP_200
            resp.content_type = ['application/json']
            resp.body = json.dumps({"status":"success", "code":200, "message":"Event logged to the database."})

        except Exception as e:
            get_logger().error(e, exc_info=True)

            # Inserting the entry failed, return http_400
            resp.status = falcon.HTTP_400
            resp.content_type = ['application/json']
            resp.body = json.dumps({"status":"error", "code":400, "message":"Failed to log event to the database"})
