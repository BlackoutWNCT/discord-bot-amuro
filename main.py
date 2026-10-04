
import discord, logging, os, argparse, sys

from card_lookup import card_find
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
from pathlib import Path

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument(
    "--environment",
    choices=["prod","dev"],
    default="dev"
)

args = parser.parse_args()
env = args.environment
start_time = datetime.now().strftime("%Y%m%d-%H%M%S")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

amuro_logger = logging.getLogger("amuro_logger")
root_logger = logging.getLogger()

if env == "dev":
    auth_token = os.getenv('DISCORD_TOKEN_DEV')

    log_level = logging.DEBUG
    log_dir = Path("./")

    log_formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(name)s: %(message)s")

    amuro_logger.setLevel(log_level)
    root_logger.setLevel(log_level)

    print(f"Launching Amuro in DEV mode")

elif env == "prod":
    auth_token = os.getenv('DISCORD_TOKEN_PROD')

    log_level = logging.WARNING
    log_dir = Path("/var/log/discord-amuro")

    log_formatter = logging.Formatter("%(levelname)s: %(message)s")

    amuro_logger.setLevel(logging.INFO)
    root_logger.setLevel(log_level)

    print(f"Launching Amuro in PROD mode")

else:
    print("Invalid env argument")

log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f'amuro-{start_time}.log'

log_handler = logging.FileHandler(filename=log_file, 
                            encoding='utf-8', 
                            mode='w')

journal_handler = logging.StreamHandler(sys.stderr)

handlers = [log_handler, journal_handler]

for handler in handlers:
    handler.setFormatter(log_formatter)
    root_logger.addHandler(handler)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.check
async def globally_check(ctx):
    if any(role.name == "Pilot" for role in ctx.author.roles) == False:
        await ctx.author.send(f'You do not have permission to invoke commands, please visit #server-rules to resolve this')
        await ctx.message.delete()
        amuro_logger.warning(f'{ctx.author.display_name} (ID: {ctx.author.id}) attempted to invoke a command without the appropriate role')
    else:
        return True

@bot.event
async def on_ready():
    amuro_logger.info(f'{bot.user.name} is ready and standing by...')

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong {ctx.author.mention}!")

@bot.command()
async def card(ctx, *, content):

    card_data = card_find(content)

    if card_data == None:
        await ctx.send(f'The requested card doesn\'t appear to exist ({content.upper()}). Please try again')
        await ctx.message.delete()
        amuro_logger.warning(f'{ctx.author.display_name} (ID: {ctx.author.id}) requested card info for an invalid card: {content}.')

    else:
        await ctx.send(f'Card Name: {card_data["Name"]} \n'
                    f'Card Number: [{card_data["Code"]}]({card_data["Image_Url"]}) \n'
                    f'Card Effect:```{card_data["Effect"]}```'
                    )
        await ctx.message.delete()
        amuro_logger.info(f'{ctx.author.display_name} (ID: {ctx.author.id}) requested card info for card: {content}. The request was successful.')

@bot.command()
async def lfg(ctx):

    if ctx.channel.name == "lfg":

        lfg_id = discord.utils.get(ctx.guild.roles, name="LFG")

        if lfg_id in ctx.author.roles:
            await ctx.author.remove_roles(lfg_id)
            await ctx.send(f'{ctx.author.mention} is no longer looking for a game')
            amuro_logger.info(f'{ctx.author.display_name} (ID: {ctx.author.id}) invoked lfg; the role was revoked.')
        else:
            await ctx.author.add_roles(lfg_id)
            await ctx.send(f'{lfg_id.mention} - {ctx.author.mention} is looking for a game')
            amuro_logger.info(f'{ctx.author.display_name} (ID: {ctx.author.id}) invoked lfg; the role was assigned.')
    else:
        await ctx.author.send(f'Please use the [#lfg](https://discord.com/channels/1404061057877676042/1552576562216435853) channel to issue the \"!lfg\" command. Thank you.')
        amuro_logger.warning(f'{ctx.author.display_name} (ID: {ctx.author.id}) invoked lfg; the channel was invalid and they were notified.')
 
    await ctx.message.delete()

bot.run(auth_token, log_handler=None, log_level=log_level)