import yfinance as yf
import datetime
import pandas as pd
import json

sma = 5
lma = 20

print('RUNING TECHNICAL ANALYSIS')

def extract_symbols(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            keys = list(data.keys())
            return keys
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return []

symbol_list = extract_symbols(r'C:\Users\David\Documents\ProfitPilot\V5\results\TB_nalysed_stocks.json')

def get_price_data(symbol_list, sma, lma, days_num, json_path, interval):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days_num)
    
    all_data = {}
    
    for symbol in symbol_list:
        try:
            data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
            df = data.reset_index()

            df['SMA'] = df['Close'].rolling(sma).mean()
            df['LMA'] = df['Close'].rolling(lma).mean()

            df['MACD'] = df['SMA'] - df['LMA']
            df['SL'] = df['MACD'].rolling(window=9, min_periods=1).mean()

            inter_df = df.iloc[19:]
            inter_df['SMA/LMA'] = inter_df.apply(lambda row: 1 if row['SMA'] > row['LMA'] else 0, axis=1)
            inter_df['MACD/SL'] = inter_df.apply(lambda row: 1 if row['MACD'] > row['SL'] else 0, axis=1)
            
            # Store additional data in the JSON file
            all_data[symbol] = {
                'sma/lma': int(inter_df['SMA/LMA'].iloc[-1]),
                'macd/sl': int(inter_df['MACD/SL'].iloc[-1])
            }
            
            # Save additional data to the JSON file
            with open(json_path, 'w') as json_file:
                json.dump(all_data, json_file)

        except Exception as e:
            print(f"Error retrieving data for {symbol}: {e}")

    return all_data

#7-1h
days_num = 7
interval = '1h'
file_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\1h.json'
get_price_data(symbol_list, sma, lma, days_num, file_path, interval)
#3-15m
days_num = 3
interval = '15m'
file_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\15m.json'
get_price_data(symbol_list, sma, lma, days_num, file_path, interval)
#30-1d
days_num = 30
interval = '1d'
file_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\1d.json'
get_price_data(symbol_list, sma, lma, days_num, file_path, interval)
#365-5d
days_num = 365
interval = '5d'
file_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\5d.json'
get_price_data(symbol_list, sma, lma, days_num, file_path, interval)

'''
intervals to test:
daysnum     interval
7           1h
3           15m
30          1d
365         5D         

OUTPUT:
sma/lma : 1/0
macd/sl : 1/0
'''

# Available intervals for historical price data retrieval:
# '1m': One-minute interval
# '2m': Two-minute interval
# '5m': Five-minute interval
# '10m': Ten-minute interval
# '15m': Fifteen-minute interval
# '30m': Thirty-minute interval
# '1h': One-hour interval
# '90m': Ninety-minute interval
# '1d': Daily interval
# '5d': Five-day interval (business days)
# '1wk': Weekly interval
# '1mo': Monthly interval
print(symbol_list)