import discord
from discord.ext.commands import Bot
from discord import Embed
import datetime
import pygsheets
import pandas as pd
import os


BOT_PREFIX = "!"
BOT_TOKEN = os.environ.get("Snowflake_BOT_TOKEN")
client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.command(name="greet")
async def greeting(ctx):
    await ctx.send("Hello")


# runs when bot is started ----- not seen in server
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


client.run(BOT_TOKEN)
