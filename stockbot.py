import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready')

@client.event 
async def on_member_join(member):
    print(f'{member} has joined the server!')

@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is {round(client.latency * 1000)} ms')


client.run(os.getenv('TOKEN'))