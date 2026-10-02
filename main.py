
import discord, logging, os, argparse

from card_lookup import card_find
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "--environment",
    choices=["prod","dev"],
    default="dev"
)

args = parser.parse_args()
env = args.environment

load_dotenv()

if env == "dev":
    token = os.getenv('DISCORD_TOKEN_DEV')
    print(f"Launching Amuro in DEV mode")

    log_level = logging.DEBUG

    log_dir = Path("./")
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = log_dir / f'amuro-{timestamp}.log'

    handler = logging.FileHandler(filename=log_file, 
                                encoding='utf-8', 
                                mode='w')

elif env == "prod":
    token = os.getenv('DISCORD_TOKEN_PROD')
    print(f"Launching Amuro in PROD mode")

    log_level = logging.ERROR

    log_dir = Path("/var/log/Discord-Amuro")
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = log_dir / f'amuro-{timestamp}.log'

    handler = logging.FileHandler(filename=log_file, 
                                encoding='utf-8', 
                                mode='w')
else:
    print("Invalid env argument")

intents = discord.Intents.default()

intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.check
async def globally_check(ctx):
    if any(role.name == "Pilot" for role in ctx.author.roles) == False:
        await ctx.author.send(f'You do not have permission to invoke commands, please visit #server-rules to resolve this')
        await ctx.message.delete()
    else:
        return True

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready and standing by...")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong {ctx.author.mention}!")

@bot.command()
async def card(ctx, *, content):

    card_data = card_find(content)

    if card_data == None:
        await ctx.send(f'The requested card doesn\'t appear to exist ({content.upper()}). Please try again')
        await ctx.message.delete()

    else:
        await ctx.send(f'Card Name: {card_data["Name"]} \n'
                    f'Card Number: [{card_data["Code"]}]({card_data["Image_Url"]}) \n'
                    f'Card Effect:```{card_data["Effect"]}```'
                    )
        await ctx.message.delete()

bot.run(token, log_handler=handler, log_level=log_level)