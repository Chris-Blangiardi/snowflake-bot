import datetime
import os

import pandas as pd
import pygsheets
from discord import Embed
from discord.ext.commands import Bot

BOT_PREFIX = "!"
BOT_TOKEN = os.environ.get("Snowflake_BOT_TOKEN")
client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.command(name="greet")
async def greeting(ctx):
    await ctx.send("Hello {}".format(ctx.author.name))


@client.command(name="sheets")
async def pokemon(ctx):
    gc = pygsheets.authorize(service_account_env_var="GoogleSheetsAPI")
    # open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sheet = gc.open("Pokemon Nuzlockes")
    # select the first sheet
    wks = sheet.sheet1

    column_data = wks.get_row(row=1)
    row_data = wks.get_col(col=1, include_tailing_empty=False)

    df = pd.DataFrame(data=wks, columns=column_data, index=row_data)

    embed = Embed(title="Pokemon", description="Black And White 2", url=os.getenv("GoogleSheetData"),
                  colour=0x0000FF, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Current Stats", value=df.to_string(header=None, index=None, max_colwidth=True), inline=False)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3"
                            "%A9mon_logo.svg/1200px-International_Pok%C3%A9mon_logo.svg.png")

    message = await ctx.send(embed=embed)

    await message.add_reaction('🇷')
    await message.add_reaction('🇩')
    await message.add_reaction('🇵')

    while True:
        react = await client.wait_for('reaction_add')

        if str(react[0]) == "🇷":
            df.at["{}".format(react[1]), "Restarts"] = int(df.at["{}".format(react[1]), "Restarts"]) + 1
            await message.remove_reaction("🇷", react[1])
        elif str(react[0]) == "🇩":
            df.at["{}".format(react[1]), "Deaths"] = int(df.at["{}".format(react[1]), "Deaths"]) + 1
            await message.remove_reaction("🇩", react[1])
        elif str(react[0]) == "🇵":
            df.at["{}".format(react[1]), "PB"] = int(df.at["{}".format(react[1]), "PB"]) + 1
            await message.remove_reaction("🇵", react[1])

        wks.set_dataframe(df, (0, 0))
        wks.delete_rows(1)

        embed_update = Embed(title="Pokemon", description="Black And White 2", url=os.getenv("GoogleSheetData"),
                             colour=0x0000FF, timestamp=datetime.datetime.utcnow())
        embed_update.add_field(name="Current Stats", value=df.to_string(header=None, index=None), inline=False)
        embed_update.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98"
                                       "/International_Pok%C3"
                                       "%A9mon_logo.svg/1200px-International_Pok%C3%A9mon_logo.svg.png")
        await message.edit(embed=embed_update)


# runs when bot is started ----- not seen in server
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


client.run(BOT_TOKEN)
