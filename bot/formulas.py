import json

def percentage_growth(now, prev):
    try:
        return round((float((float(now) - float(prev)) / abs(float(prev))) * 100), 2)
    except ZeroDivisionError:
        return 'Dividing by zero'
    except TypeError:
        return 'Formatting problem'
    except ValueError:
        return 'Formatting problem'

def parse_data(data):
    return json.dumps(data).replace('"', '')

def gross_margin(revenue, grossprofit):
    return round(float((float(grossprofit) / float(revenue)) * 100), 2)

#def eps_output(eps):
    

# {earnings_data[i]['fiscalDateEnding']}