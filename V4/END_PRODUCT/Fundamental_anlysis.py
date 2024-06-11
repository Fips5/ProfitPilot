import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import requests

API_KEY ='pV7EpV25UlOaPEsj6iWW9sAKTSMtz41I'
symbol = "AAPL"
year = "2023"
period = "quarter" #CAN BE "quarter" OR "annul"

calendar_start = '2023-06-10'       #YYYY - MM - DD
calendar_end = '2023-08-10'         #YYYY - MM - DD

annual_period = 'FY'  #, 'Q1', 'Q2', 'Q3', 'Q4'
annual_year = 2023  #just the year

def df_to_excel(df, file_path):
    try:
        df.to_excel(df, index=False)
        print("DataFrame successfully saved to Excel file:", file_path)
    except Exception as e:
        print("An error occurred while saving the DataFrame to Excel:", e)
   


def extract_unique_keys(data):
    unique_keys = set()
    for entry in data:
        unique_keys.update(entry.keys())
    return list(unique_keys)

def extract_api(the_url):
  response = requests.get(the_url)
  json_data = response.json()
  return json_data

def json_to_df(the_url):
  json_data = extract_api(the_url)
  if isinstance(json_data, list):
    keys = extract_unique_keys(json_data)
    df = pd.DataFrame(json_data, columns=keys)
    return df
  else:
    print("Expected JSON data, but received:", json_data)

income_url =  (f'https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=annual&apikey={API_KEY}')

balance_sheet_url =  (f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?period=annual&apikey={API_KEY}")

'''

example to get the data out of the api and into a pandas df
the_url1 = balance_sheet_url
df = json_to_df(balance_sheet_url)
print(df)
print(balance_sheet_url)
df.df

'''

the_url1 = balance_sheet_url
df = json_to_df(balance_sheet_url)
print(df)
print(balance_sheet_url)

anual_raport = 1
quarterly_ralory = 2

#df_to_excel(df, file_path)