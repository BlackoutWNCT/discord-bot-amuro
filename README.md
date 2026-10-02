# discord-bot-amuro
Amuro Discord bot for Gundam TCG Perth discord server

## Commands
### !card
Looks up a card using the card ID.

Example: `!card GD01-001`

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
 - View Channels
 - Send Messages
 - Manage Messages
 - Read Message History

