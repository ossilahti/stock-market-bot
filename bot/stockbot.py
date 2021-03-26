import os
import discord
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
            await ctx.send(f"""Ticker: {question.upper()}\nP/E: {data['PERatio']}\nP/B: {data['PriceToBookRatio']}\nP/S: {data['PriceToSalesRatioTTM']}\nDividend yield: {data['DividendYield']}%""")
        else:
            await ctx.send(f'API Returned a {response.status} status' )
   

@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is {round(client.latency * 1000)} ms')

client.run(os.getenv('TOKEN'))