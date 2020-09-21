# Author: @Travis-Owens
# Date: 2020-08-27
# Description: I can't get cron to run inside docker, so using this instead
# Non-busy sleep, https://www.python.org/dev/peps/pep-0475/

from time import sleep

from twitch_oauth import twitch_oauth
from twitch_subscribe import twitch_subscribe
from cron_test import cron_test

while True:
    try:
        # cron_test()
        twitch_oauth()
        twitch_subscribe()
        sleep(60*60)
    except Exception as e:
        print(str(e))
