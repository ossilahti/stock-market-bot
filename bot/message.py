import discord

def parse_data(data):
    for i in data:
        if (data[i] != 'PERatio'):
            del data[i]
