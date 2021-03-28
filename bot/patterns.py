import discord

def rev_growth(data_now, data_prev):
    growth = round((float((int(data_now)-int(data_prev)) / int(data_prev)) * 100), 2)
    return growth

