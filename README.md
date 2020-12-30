# keshbotics3
This is the third iteration of the KeshBotics Discord chat bot.

This bot has three semi-independent systems: API, crontab, and Discord async.

Primary Functionality:
- Post message to discord when defined twitch user's begin streaming.
- Discord chat interface for managing notifications.

# Overview
## API
  This module is based on the Falcon framework.
  Functions:
  - Twitch
    - add, delete: webhook subscriptions
    - Receive/process twitch webhook POST

## crontab
  This module will re-subscribe to Twitch webhook POST for each twitch user.
  - Twitch webhook subscriptions expire after x-amount of time.
  - Due to issues with running crontab inside of docker, these functions are no handled by crontab/cron_run.py.

## discord_async
  Discord chat bot built using discord.py (https://pypi.org/project/discord.py/)

  Functions:
  - Add/Delete notifications via chat commands


# Installation / Usage
## Docker Container Building and Running
  TODO: Create instructions detailing KeshBotics setup

  Build:

    docker build -t keshbotics:v3 .

  Run:

    docker run -d --network="host" --env-file=keshbotics.env keshbotics:v3


## Notification Setup
  1. Determine the discord channel that the twitch notification should be sent to.
  2. Use this command to create the notification:


    k!twitch add <twitch username>

## Notification Deletion
  1. In the corresponding discord channel user this command:


    k!twitch del <twitch username>
