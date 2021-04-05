import os
import json
from dotenv import load_dotenv
from aiohttp import request
load_dotenv()

market_key = os.getenv('MARKET')

async def get_income_data(question):

    async with request('GET', f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={question}&apikey={market_key}", headers={}) as response:
        if response.status == 200:
            return await response.json()
        else:
            raise Exception("Failed to retrieve company's income data.")

async def get_company_overview(question):
    
    async with request('GET', f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={question}&apikey={market_key}", headers={}) as response:
        if response.status == 200:
            return await response.json()
        else:
            raise Exception('Failed to retrieve data of company overview.')

async def get_earnings(question):

    async with request('GET', f"https://www.alphavantage.co/query?function=EARNINGS&symbol={question}&apikey={market_key}", headers={}) as response:
        if response.status == 200:
            return await response.json()
        else:
            raise Exception("Failed to retrieve data of company's earnings")