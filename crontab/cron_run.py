# Author: @Travis-Owens
# Date: 2020-08-27
# Description: I can't get cron to run inside docker, so using this instead
# Non-busy sleep, https://www.python.org/dev/peps/pep-0475/

from time import sleep

from twitch_oauth import twitch_oauth
from twitch_subscribe import twitch_subscribe
from youtube_subscribe import youtube_subscribe

while True:
    try:
        # Creates a new Twitch oath token and stores it in the database
        twitch_oauth()

        # Resubscribes to webhook notifications for each unique Twitch user ID in the database
        twitch_subscribe()

        # Resubscribes to webhook notifications for each unique YouTube channel ID in the database
        youtube_subscribe()

        sleep(60*60)
    except Exception as e:
        # TODO: Logging implementation
        print(str(e))
