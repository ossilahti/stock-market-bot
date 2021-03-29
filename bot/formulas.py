import discord
import json

def percentage_growth(now, prev):
    return round((float((float(now) - float(prev)) / abs(float(prev))) * 100), 2)
    
def parse_data(data):
    return json.dumps(data).replace('"', '')

def gross_margin(now, prev):
    return round((float((float(now) - float(prev)) / abs(float(now))) * 100), 2)