# Author: @Travis-Owens
# Date: 2020-08-27
# Description: I can't get cron to run inside docker, so using this instead
# Non-busy sleep, https://www.python.org/dev/peps/pep-0475/

from time import sleep
import requests

from twitch_oauth import twitch_oauth
from youtube_subscribe import youtube_subscribe

# Wait for API to start
sleep(30)

while True:
    try:
        twitch_oauth()                  # Updates the oauth token for the Twitch API
        youtube_subscribe()             # Resubscribes to YouTube webhook events
        sleep(60*60*23)                 # 82,800 seconds (23 hours)
    except Exception as e:
        print(e)
