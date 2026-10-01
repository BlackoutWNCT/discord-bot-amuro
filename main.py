
import discord
import logging
import os
import argparse

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

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, Your content has been deleted for violating community standards")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def card(ctx):
    await ctx.send('https://www.gundam-gcg.com/en/images/cards/card/GD01-001.webp?260917')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)