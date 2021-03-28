import discord
import json

def revenue_growth(data_now, data_prev):
    return round((float((int(data_now)-int(data_prev)) / int(data_prev)) * 100), 2)


def eps_growth(now, prev):
    return round((float((float(now) - float(prev)) / abs(float(prev))) * 100), 2)
    

def parse_data(data):
    return json.dumps(data).replace('"', '')
    