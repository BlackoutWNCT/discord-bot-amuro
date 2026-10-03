# discord-bot-amuro
Amuro Discord bot for Gundam TCG Perth discord server

## Commands
### !card
Looks up a card using the card ID.

Example: `!card GD01-001`

### !lfg
Determines if the user is currently assigned the lfg (Looking for Game) role and either assigns it to them or revokes it.
Also pings the role in the lfg channel to notify other users who are looking for a game that a new player is searching.
Messages are restricted to the "#lfg" channel, invoking the command anywhere else will result in the user receiving a DM from the bot.

Example: `!lfg`

## Virtual Env
`python3 -m venv bot-env`

`source ./bot-env/bin/activate`

## Install required packages
`pip install -r ./requirements.txt`


## Permissions Required
### Privileged Gateway Intents:
 - Server Members Intent
 - Message Content Intent

### Bot Permissions (OAuth2 Scopes):
 - URL Generator = bot
 - Manage Roles
 - View Channels
 - Send Messages
 - Manage Messages
 - Read Message History