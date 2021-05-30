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


def googleSheets():
    key = os.environ.get("GoogleSheetsAPI")
    gc = pygsheets.authorize(service_file=key)
    # open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sheet = gc.open("PY to Gsheet Test")
    # select the first sheet
    wks = sheet.sheet1

    column_data = wks.get_row(row=1)
    row_data = wks.get_col(col=1, include_tailing_empty=False)

    df = pd.DataFrame(data=wks, columns=column_data, index=row_data)

    # update the first sheet with df.
    wks.set_dataframe(df, (0, 0))
    wks.delete_rows(1)
    return df


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.command(name="greet")
async def greeting(ctx):
    await ctx.send("Hello {}".format(ctx.author.name))


@client.command(name="sheets")
async def pokemon(ctx):
    embed = Embed(title="Pokemon", description="Black And White 2",
                  colour=0x0000FF, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Current Stats", value=None, inline=False)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3"
                            "%A9mon_logo.svg/1200px-International_Pok%C3%A9mon_logo.svg.png")

    message = await ctx.send(embed=embed)

    await message.add_reaction('🇷')
    await message.add_reaction('🇩')
    await message.add_reaction('🇵')

    while True:
        react = await client.wait_for('reaction_add')

        if str(react[0]) == "🇷":
            await message.remove_reaction("🇷", ctx.author)
        elif str(react[0]) == "🇩":
            await message.remove_reaction("🇩", ctx.author)
        elif str(react[0]) == "🇵":
            await message.remove_reaction("🇵", ctx.author)


# runs when bot is started ----- not seen in server
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


client.run(BOT_TOKEN)
