# Author: @Travis-Owens
# Date: 2020-02-26
# Description: Used to collect information about streamming habbits


import datetime
from classes.data_handler import data_handler

class stream_metrics(object):
    def __init__(self):
        pass

    def stream_start(self, twitch_user_id):
        try:
            sql = "INSERT INTO `stream_metrics_time` VALUES (null, %s, NOW(), null)"
            x = data_handler().insert(sql, [twitch_user_id])
        except:
            print('stream_metrics: 1')
            pass

    def stream_stop(self, twitch_user_id):
        try:
            sql     = "SELECT `id` FROM `stream_metrics_time` WHERE `twitch_user_id` = %s AND `stream_stop` IS NULL ORDER BY `id` DESC LIMIT 1"
            data    = data_handler().select(sql, [twitch_user_id])
            id      = data[0]['id']

            sql = "UPDATE `stream_metrics_time` SET `stream_stop`=NOW() WHERE `id`=%s"
            result = data_handler().update(sql, [id])

        except Exception as e:
            print('stream_metrics: 2')
            print(e)
            pass

    def get_stream_metrics(self, twitch_user_id, limit=10):

        # Prepare dict for return values
        return_data = {'twitch_user_id':twitch_user_id,
            'streams':[

            ],
            'total':0
            }

        # Retreive stream_start, stream_stop data
        sql = "SELECT `stream_start`, `stream_stop` FROM `stream_metrics_time` WHERE `twitch_user_id` = %s ORDER BY `id` DESC LIMIT %s"
        input = [twitch_user_id, limit]
        data = data_handler().select(sql, input)

        # Object for storing the total length of broadcast
        total_time = datetime.timedelta()

        for stream in data:
            try:
                # Compute the lenght of the stream and add to total_time
                time = stream['stream_stop']-stream['stream_start']
                total_time += time

                # Convert time objects to string
                stream['time'] = str(time)
                stream['stream_start'] = str(stream['stream_start'])
                stream['stream_stop'] = str(stream['stream_stop'])

                # Append formated stream information to return_data
                return_data['streams'].append(stream)

            except Exception as e:
                print('stream_metrics: 3')

                pass


        # Sort the list of streams to be chronological
        return_data['streams'].reverse()

        # Add str value of total_time to return data
        return_data['total'] = str(total_time)

        return(return_data)
