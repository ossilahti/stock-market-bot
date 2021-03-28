import os
import discord
import json
import re
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from pprint import pprint
from aiohttp import request
load_dotenv()

client = commands.Bot(command_prefix = '.')
tokenkey = os.getenv('TOKEN')

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def f(ctx, *, question):

    URL = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={question}&apikey={tokenkey}'
    async with request('GET', URL, headers={}) as response:
        if response.status == 200:
            data = await response.json()
            json_string = json.dumps(data['Description'])
            json_string = ' '.join(re.split(r'(?<=[.])\s', json_string)[:3])

            embed = Embed(title=f"{data['Name']} - ({question.upper()})",
                          description = json_string[1:],
                          colour = 0x2ecc71)
                
            embed.add_field(name = 'Fundamentals', 
                            value = f"""P/E: {data['PERatio']}\nP/B: {data['PriceToBookRatio']}\nP/S: {data['PriceToSalesRatioTTM']}\nDividend yield: {data['DividendYield']}""", 
                            inline = True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'API Returned a {response.status} status' )
   

@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is {round(client.latency * 1000)} ms')

client.run(os.getenv('TOKEN'))