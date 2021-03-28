import os
import discord
import json
import re
from patterns import *
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
    URL2 = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={question}&apikey={tokenkey}'

    async with request('GET', URL2, headers={}) as response:
        if response.status == 200:
            income_data = await response.json()
            income_data = income_data['annualReports']
            rev_data1 = json.dumps(income_data[0]['totalRevenue']).replace('"', '')
            rev_data2 = json.dumps(income_data[1]['totalRevenue']).replace('"', '')
            growth = rev_growth(rev_data1, rev_data2)
        else:
            await ctx.send(f'API Returned a {response.status} status' )

    async with request('GET', URL, headers={}) as response:
        if response.status == 200:
            data = await response.json()

            description = json.dumps(data['Description'])
            description = ' '.join(re.split(r'(?<=[.])\s', description)[:3])
            dividend = json.dumps(data['DividendYield']).replace('"', '')
            dividend = round(float(dividend) * 100, 2)

            embed = Embed(title=f"{data['Name']} - ({question.upper()})",
                          description = description[1:],
                          colour = 0x2ecc71)
                
            embed.add_field(name = 'Fundamentals', 
                            value = f"P/E: {data['PERatio']}\nP/B: {data['PriceToBookRatio']}\nP/S: {data['PriceToSalesRatioTTM']}\nForward P/E: {data['ForwardPE']}\nEV/Revenue: {data['EVToRevenue']}\nDividend yield: {dividend} %", 
                            inline = True)

            embed.add_field(name = 'Growth',
                            value = f"Revenue Growth: {growth} %",
                            inline = True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'API Returned a {response.status} status' )
   

@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is {round(client.latency * 1000)} ms')

client.run(os.getenv('TOKEN'))