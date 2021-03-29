import os
import discord
import json
import re
from httpqueries import get_income_data, get_company_overview, get_earnings
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

    # Income data
    try: 
        response_json = await get_income_data(question)
        income_data = response_json['annualReports']
        rev_data1 = parse_data(income_data[0]['totalRevenue'])
        rev_data2 = parse_data(income_data[1]['totalRevenue'])
        net_income_now = parse_data(income_data[0]['netIncome'])
        net_income_prev = parse_data(income_data[1]['netIncome'])
        cost_of_goods = parse_data(income_data[0]['costofGoodsAndServicesSold'])
    except:
        await ctx.send('API failed to connect to Income Data.')

    # Earnings data
    try:
        earnings_json = await get_earnings(question)
        earnings_data = earnings_json['annualEarnings']
        earnings_now = parse_data(earnings_data[0]['reportedEPS'])
        earnings_prev = parse_data(earnings_data[1]['reportedEPS'])
    except:
        await ctx.send('API failed to connect to Earnings Data.')    

    # Company overview data
    try:
        data = await get_company_overview(question)
        description = json.dumps(data['Description'])
        description = ' '.join(re.split(r'(?<=[.])\s', description)[:2])

        dividend = parse_data(data['DividendYield'])
        dividend = round(float(dividend) * 100, 2)

        roa = round(float(parse_data(data['ReturnOnAssetsTTM'])) * 100, 2)
        roe = round(float(parse_data(data['ReturnOnEquityTTM'])) * 100, 2)
        operating_margin = round(float(parse_data(data['OperatingMarginTTM'])) * 100, 2)
        profit_margin = round(float(parse_data(data['ProfitMargin'])) * 100, 2)

        embed = Embed(title=f"{data['Name']} - ({question.upper()})",
                        description = description[1:],
                        colour = 0x2ecc71)
                
        embed.add_field(name = 'Valuation', 
                        value = f"P/E: {data['PERatio']}\nP/B: {data['PriceToBookRatio']}\nP/S: {data['PriceToSalesRatioTTM']}\nForward P/E: {data['ForwardPE']}\nEV/Revenue: {data['EVToRevenue']}\nDividend rate: {dividend} %", 
                        inline = True)

        embed.add_field(name = 'Growth (YoY)',
                        value = f"Revenue Growth: {percentage_growth(rev_data1, rev_data2)} %\nEPS Growth: {percentage_growth(earnings_now, earnings_prev)} %\nNet Income Growth: {percentage_growth(net_income_now, net_income_prev)} %",
                        inline = True)

        embed.add_field(name = 'Effectiveness & Profitability',
                        value = f"ROA: {roa} %\nROE: {roe} %\nGross margin: {gross_margin(rev_data1, cost_of_goods)} %\nOperating margin: {operating_margin} %\nProfit margin: {profit_margin} %",
                        inline = False)
        await ctx.send(embed=embed)
    except:
        await ctx.send('API failed to connect to Company Overview.')
   

@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is {round(client.latency * 1000)} ms')

client.run(os.getenv('TOKEN'))