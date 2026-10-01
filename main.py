
import discord, logging, os, argparse

from card_lookup import card_find
from dotenv import load_dotenv
from discord.ext import commands

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
elif env == "prod":
    token = os.getenv('DISCORD_TOKEN_PROD')
    print(f"Launching Amuro in PROD mode")
else:
    print("Invalid env argument")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()

intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

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
        await ctx.send(f'The request was invalid, please try again')

    else:
        await ctx.send(f'Card Name: {card_data["Name"]} \n'
                    f'Card Number: [{card_data["Code"]}]({card_data["Image_Url"]}) \n'
                    f'Card Effect:```{card_data["Effect"]}```'
                    )

bot.run(token, log_handler=handler, log_level=logging.DEBUG)