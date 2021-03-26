import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from pprint import pprint
load_dotenv()

client = commands.Bot(command_prefix = '.')


def callbackfunc(question):
    fd = FundamentalData(key=os.getenv('TOKEN'), output_format='pandas')
    data, meta_data = fd.get_company_overview(symbol=question)
    print(data['PERatio'])
    print(data['PriceToSalesRatioTTM'])
    print(data['PriceToBookRatio'])
    print(data['ForwardAnnualDividendYield'])

@client.event
async def on_ready():
    print('Bot is ready')

@client.event 
async def on_member_join(member):
    print(f'{member} has joined the server!')

@client.command()
async def f(ctx, *, question):
    await ctx.send(f'Ticker: {question}\nStats: {callbackfunc(question)}')

@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is {round(client.latency * 1000)} ms')

client.run(os.getenv('TOKEN'))