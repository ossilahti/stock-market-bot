import os
import discord
import json
import re
from httpqueries import get_company_overview, get_earnings, get_income_data, get_timeseries
from formulas import percentage_growth,  gross_margin, parse_data
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv
from aiohttp import request
from tabulate import tabulate
load_dotenv()

client = commands.Bot(command_prefix = '.')
tokenkey = os.getenv('MARKET')

@client.event
async def on_ready():
    print('Bot is ready')

@client.command(aliases=['earnings'])
async def e(ctx, *, question):
    try:
        eps = []
        earnings_json = await get_earnings(question)
        earnings_data = earnings_json['annualEarnings']

        for i in range(len(earnings_data)):
            if i < 10:
                eps.append(parse_data(earnings_data[i]['reportedEPS']))

        epsstring = ""
        for index in range(len(eps)):
            epsstring += f"{earnings_data[index]['fiscalDateEnding']}         | {eps[index]}\n"
        header_eps = "Fiscal year ending | EPS\n-------------------------\n"
    except:
        await ctx.send(f'Could not find more than {i} year(s) of data')

    try:
        data = await get_company_overview(question)
        embed = Embed(title=f"Earnings data for {data['Name']}",
                    colour = 0x2ecc71)

        embed.add_field(name = "Development",
                        value = f"```{header_eps}{epsstring}```")
        await ctx.send(embed=embed)
    except:
        await ctx.send('Could not send the message')


@client.command(aliases=['funda'])
async def f(ctx, *, question):

    # Income data
    try: 
        response_json = await get_income_data(question)
        income_data = response_json['annualReports']
        rev_now = parse_data(income_data[0]['totalRevenue'])
        rev_prev = parse_data(income_data[1]['totalRevenue'])
        net_income_now = parse_data(income_data[0]['netIncome'])
        net_income_prev = parse_data(income_data[1]['netIncome'])
        gross_profit = parse_data(income_data[0]['grossProfit'])
    except:
        await ctx.send(f"Can't bring income data for {question.upper()}. IPO'ed last year?")

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
                        value = f"Revenue Growth: {percentage_growth(rev_now, rev_prev)} %\nNet Income Growth: {percentage_growth(net_income_now, net_income_prev)} %",
                        inline = True)

        embed.add_field(name = 'Effectiveness & Profitability',
                        value = f"ROA: {roa} %\nROE: {roe} %\nGross margin: {gross_margin(rev_now, gross_profit)} %\nOperating margin: {operating_margin} %\nProfit margin: {profit_margin} %",
                        inline = False)

    except: 
        await ctx.send(f"Could not bring company overview for {question.upper()}.")
    try:
        await ctx.send(embed=embed)
    except:
        await ctx.send('Could not send the information about the stock')
    

@client.command(aliases=['price'])
async def p(ctx, *, question):
    response_json = await get_timeseries(question)
    metadata = response_json['Meta Data']
    timeseries = response_json['Time Series (Daily)'][metadata['3. Last Refreshed']]
    
    try:
        embed = Embed(title=f"Daily time series for {question.upper()}",
                      description = f"Last refreshed: {metadata['3. Last Refreshed']}",
                      colour = 0xc27c0e)
        embed.add_field(name = 'Time series',
                        value= f"```Open:   {timeseries['1. open']}\nHigh:   {timeseries['2. high']}\nLow:    {timeseries['3. low']}\nClose:  {timeseries['4. close']}\nVolume: {timeseries['6. volume']}```",
                        inline=False)
        await ctx.send(embed=embed) 
    except:
        await ctx.send('Could not send the time series of the stock')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(f'That is not a command!')

client.run(os.getenv('TOKEN'))