import pandas as pd
import numpy as np
from datetime import datetime
import openpyxl
import json
import time

#test buy, sell close:

#from tbuy import buy
#from tclose import close
#from tsell import sell

#actul buy, sell, close(comment out to run test):

#from buy import buy
#from close import close
#from sell import sell()

TIME = 53
#Indicatori:
SMA = 7
LMA = 24
PVTW = 10
HGW = 10
#Setari Pozitii:
STOPLOSSP = 0.9
TAKEPROFITP= 1
TSP = STOPLOSSP * 0.001 #teiling stoploss, the formula i use is 
TTP = TAKEPROFITP * 0.002
SP = 0.003
TP = 0.0015

SP_P = 0.002
ATRP = 14

json_paths = [
    r'C:\Users\David\Desktop\Fundamental_analysis\json_prices\price_1.json',
    r'C:\Users\David\Desktop\Fundamental_analysis\json_prices\price_2.json',
    r'C:\Users\David\Desktop\Fundamental_analysis\json_prices\price_3.json',
    r'C:\Users\David\Desktop\Fundamental_analysis\json_prices\price_4.json',
    r'C:\Users\David\Desktop\Fundamental_analysis\json_prices\price_5.json',
    r'C:\Users\David\Desktop\Fundamental_analysis\json_prices\price_6.json'
]

def profit_save(number):
    with open(r'C:\Users\David\Desktop\Pilot\END_PRODUCT\proft_test.txt', 'a') as file:
        file.write(f"{number} + ")

def json_to_dataframe(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    close = [item['price'] for item in data]
    dates = [item['timestamp'] for item in data]
    
    df = pd.DataFrame({'Close': close, 'Date': dates})
    
    return df

def pivot_points(series, window):
    max_val = np.max(series)
    min_val = np.min(series)
    last_val = series[-1]
    
    if last_val == max_val:
        return 1
    elif last_val == min_val:
        return -1
    else:
        return 0

def calculate_rows_until_trend_change(df):
    trend_change_index = None
    for i in range(len(df) - 1, 0, -1):
        if df['SMA'][i] > df['LMA'][i] and df['SMA'][i + 1] <= df['LMA'][i + 1]:
            trend_change_index = i
            break

    if trend_change_index is not None:
        rows_until_trend_change = len(df) - trend_change_index
    else:
        rows_until_trend_change = len(df)

    return rows_until_trend_change

def read_values_from_j(JSON_FILE_PATH):
    with open(JSON_FILE_PATH, "r") as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON at line {e.lineno}, column {e.colno}: {e.msg}")
            raise
    return data

def tp_json():
    try:
        with open(r'C:\Users\David\Desktop\Pilot\END_PRODUCT\TakeProfit.json', 'r') as json_file:
            data = json.load(json_file)
            takeprofit = data.get("take_profit")
            return takeprofit
    except FileNotFoundError:
        print("TakeProfit.json not found. Returning None.")
        return None

def tp_jsonSELL():
    try:
        with open(r'C:\Users\David\Desktop\Pilot\END_PRODUCT\TakeProfitSELL.json', 'r') as json_file:
            data = json.load(json_file)
            takeProfitSELL = data.get("take_profit")
            return takeProfitSELL
    except FileNotFoundError:
        print("TakeProfitSELL.json not found. Returning None.")
        return None
    
def sp_json():
    try:
        with open(r'C:\Users\David\Desktop\Pilot\END_PRODUCT\StopLoss.json', 'r') as json_file:
            data = json.load(json_file)
            stoploss = data.get("stop_loss")
            return stoploss
    except FileNotFoundError:
        print("StopLoss.json not found. Returning None.")
        return None

def sp_jsonSELL():
    try:
        with open(r'C:\Users\David\Desktop\Pilot\END_PRODUCT\StopLossSELL.json', 'r') as json_file:
            data = json.load(json_file)
            stopLossSELL = data.get("stop_loss")
            return stopLossSELL
    except FileNotFoundError:
        print("StopLossSELL.json not found. Returning None.")
        return None

print('STARTING PROFIT PILOT...')                   #STARTING
time.sleep(2)

pos = input("Buy position opened(y/n/s): ")
if pos.lower() == 'y':
    pos = 1
if pos.lower() == 'n':
    pos = 0


timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f'START { timestamp }')
lstpos = 0
def declare_portofolio(prices):
    path_1 = prices[0]
    path_2 = prices[1]
    path_3 = prices[2]
    path_4 = prices[3]
    path_5 = prices[4]
    path_6 = prices[5]
    
    df1 = json_to_dataframe(path_1)
    df2 = json_to_dataframe(path_2)
    df3 = json_to_dataframe(path_3)
    df4 = json_to_dataframe(path_4)
    df5 = json_to_dataframe(path_5)
    df6 = json_to_dataframe(path_6)

    df1['SMA'] = df1['Close'].rolling(SMA).mean()
    df1['LMA'] = df1['Close'].rolling(LMA).mean()
    df2['SMA'] = df2['Close'].rolling(SMA).mean()
    df2['LMA'] = df2['Close'].rolling(LMA).mean()
    df3['SMA'] = df3['Close'].rolling(SMA).mean()
    df3['LMA'] = df3['Close'].rolling(LMA).mean()
    df4['SMA'] = df4['Close'].rolling(SMA).mean()
    df4['LMA'] = df4['Close'].rolling(LMA).mean()
    df5['SMA'] = df5['Close'].rolling(SMA).mean()
    df5['LMA'] = df5['Close'].rolling(LMA).mean()
    df6['SMA'] = df6['Close'].rolling(SMA).mean()
    df6['LMA'] = df6['Close'].rolling(LMA).mean()

    df1['MACD'] = df1['SMA'] - df1['LMA']
    df1['SL'] = df1['MACD'].rolling(window=9, min_periods=1).mean()
    df2['MACD'] = df2['SMA'] - df2['LMA']
    df2['SL'] = df2['MACD'].rolling(window=9, min_periods=1).mean()
    df3['MACD'] = df3['SMA'] - df3['LMA']
    df3['SL'] = df3['MACD'].rolling(window=9, min_periods=1).mean()
    df4['MACD'] = df4['SMA'] - df4['LMA']
    df4['SL'] = df4['MACD'].rolling(window=9, min_periods=1).mean()
    df5['MACD'] = df5['SMA'] - df5['LMA']
    df5['SL'] = df5['MACD'].rolling(window=9, min_periods=1).mean()
    df6['MACD'] = df6['SMA'] - df6['LMA']
    df6['SL'] = df6['MACD'].rolling(window=9, min_periods=1).mean()

    df1['High'] = df1['Close'].shift(1).cummax()  
    df1['Low'] = df1['Close'].shift(1).cummin()
    df2['High'] = df2['Close'].shift(1).cummax()  
    df2['Low'] = df2['Close'].shift(1).cummin()
    df3['High'] = df3['Close'].shift(1).cummax()  
    df3['Low'] = df3['Close'].shift(1).cummin()
    df4['High'] = df4['Close'].shift(1).cummax()  
    df4['Low'] = df4['Close'].shift(1).cummin()
    df5['High'] = df5['Close'].shift(1).cummax()  
    df5['Low'] = df5['Close'].shift(1).cummin()
    df6['High'] = df6['Close'].shift(1).cummax()  
    df6['Low'] = df6['Close'].shift(1).cummin()

    df1['TR'] = np.maximum.reduce([
        df1['High'] - df1['Low'],
        np.abs(df1['High'] - df1['Close'].shift(1)),
        np.abs(df1['Low'] - df1['Close'].shift(1))
    ])
    df1['ATR'] = df1['TR'].rolling(window=ATRP).mean()
    df2['TR'] = np.maximum.reduce([
        df2['High'] - df2['Low'],
        np.abs(df2['High'] - df2['Close'].shift(1)),
        np.abs(df2['Low'] - df2['Close'].shift(1))
    ])
    df2['ATR'] = df2['TR'].rolling(window=ATRP).mean()
    df3['TR'] = np.maximum.reduce([
        df3['High'] - df3['Low'],
        np.abs(df3['High'] - df3['Close'].shift(1)),
        np.abs(df3['Low'] - df3['Close'].shift(1))
    ])
    df3['ATR'] = df3['TR'].rolling(window=ATRP).mean()
    df4['TR'] = np.maximum.reduce([
        df4['High'] - df4['Low'],
        np.abs(df4['High'] - df4['Close'].shift(1)),
        np.abs(df4['Low'] - df4['Close'].shift(1))
    ])
    df4['ATR'] = df4['TR'].rolling(window=ATRP).mean()
    df5['TR'] = np.maximum.reduce([
        df5['High'] - df5['Low'],
        np.abs(df5['High'] - df5['Close'].shift(1)),
        np.abs(df5['Low'] - df5['Close'].shift(1))
    ])
    df5['ATR'] = df5['TR'].rolling(window=ATRP).mean()
    df6['TR'] = np.maximum.reduce([
        df6['High'] - df6['Low'],
        np.abs(df6['High'] - df6['Close'].shift(1)),
        np.abs(df6['Low'] - df6['Close'].shift(1))
    ])
    df6['ATR'] = df6['TR'].rolling(window=ATRP).mean()

    '''
    df["high_of_trend"] = df['Close'].tail(10).max()
    df["low_of_trend"] = df['Close'].tail(10).min()
    '''

    rows1 = calculate_rows_until_trend_change(df1)
    rows2 = calculate_rows_until_trend_change(df2)
    rows3 = calculate_rows_until_trend_change(df3)
    rows4 = calculate_rows_until_trend_change(df4)
    rows5 = calculate_rows_until_trend_change(df5)
    rows6 = calculate_rows_until_trend_change(df6)

    df1["high_of_trend"] = df1['Close'].tail(rows1).max()
    df1["low_of_trend"] = df1['Close'].tail(rows1).min()
    df2["high_of_trend"] = df2['Close'].tail(rows2).max()
    df2["low_of_trend"] = df2['Close'].tail(rows2).min()
    df3["high_of_trend"] = df3['Close'].tail(rows3).max()
    df3["low_of_trend"] = df3['Close'].tail(rows3).min()
    df4["high_of_trend"] = df4['Close'].tail(rows4).max()
    df4["low_of_trend"] = df4['Close'].tail(rows4).min()
    df5["high_of_trend"] = df5['Close'].tail(rows5).max()
    df5["low_of_trend"] = df5['Close'].tail(rows5).min()
    df6["high_of_trend"] = df6['Close'].tail(rows6).max()
    df6["low_of_trend"] = df6['Close'].tail(rows6).min()

    return df1, df2, df3, df4, df5, df6

def individual_analysis(json_data_list):
    #while True:
        df1, df2, df3, df4, df5, df6 = declare_portofolio(json_data_list)
        print(df1)
        print(json_data_list[0])

individual_analysis(json_paths)
print(json_to_dataframe(json_paths[0]))



