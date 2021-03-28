import os
import discord
import json
import re
from httpqueries import get_income_data, get_company_overview
from formulas import *
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv
from aiohttp import request
load_dotenv()

client = commands.Bot(command_prefix = '.')
tokenkey = os.getenv('MARKET')

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def f(ctx, *, question):

    try: 
        response_json = await get_income_data(question)
        income_data = response_json['annualReports']
        rev_data1 = parse_data(income_data[0]['totalRevenue'])
        rev_data2 = parse_data(income_data[1]['totalRevenue'])
    except:
        await ctx.send('API failed to connect')

    try:
        data = await get_company_overview(question)
        description = json.dumps(data['Description'])
        description = ' '.join(re.split(r'(?<=[.])\s', description)[:3])

        dividend = parse_data(data['DividendYield'])
        dividend = round(float(dividend) * 100, 2)

        embed = Embed(title=f"{data['Name']} - ({question.upper()})",
                        description = description[1:],
                        colour = 0x2ecc71)
                
        embed.add_field(name = 'Fundamentals', 
                        value = f"P/E: {data['PERatio']}\nP/B: {data['PriceToBookRatio']}\nP/S: {data['PriceToSalesRatioTTM']}\nForward P/E: {data['ForwardPE']}\nEV/Revenue: {data['EVToRevenue']}\nDividend rate: {dividend} %", 
                        inline = True)

        embed.add_field(name = 'Growth',
                        value = f"Revenue Growth: {rev_growth(rev_data1, rev_data2)} %",
                        inline = True)
        await ctx.send(embed=embed)
    except:
        await ctx.send('API failed to connect')
   

@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is {round(client.latency * 1000)} ms')

client.run(os.getenv('TOKEN'))