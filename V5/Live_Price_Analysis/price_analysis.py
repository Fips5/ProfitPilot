import json
import pandas as pd 
from datetime import datetime
import numpy as np
import time

from buy import buy
from close import close

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

price_json_paths = [
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_1.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_2.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_3.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_4.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_5.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_6.json'
]

def profit_save(number):
    with open(r'C:\Users\David\Desktop\Pilot\END_PRODUCT\proft_test.txt', 'a') as file:
        file.write(f"{number} + ")

def json_price_to_df(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    
    df = pd.DataFrame(json_data)
    
    df = df.rename(columns={'price': 'Close'})
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

def main(price_json_paths, pos):
    for file_path in price_json_paths:

        df = json_price_to_df(file_path)

        file_num = file_path[58]

        print(f'FILE {file_num} : {df["Close"].iloc[-1]}')

        df['SMA'] = df['Close'].rolling(SMA).mean()
        df['LMA'] = df['Close'].rolling(LMA).mean()
        df['MACD'] = df['SMA'] - df['LMA']
        df['SL'] = df['MACD'].rolling(window=9, min_periods=1).mean()
        df['High'] = df['Close'].shift(1).cummax()  
        df['Low'] = df['Close'].shift(1).cummin()

        if pos == 0:
            openPrice = 25000

        #CONDITION:
        BuyCondition = False  
        SellCondition = False
        CloseBuy = False
        CloseSell = False

         #CONDITION  - BUY
        #and (df['MACD'].iloc[-1] > df['SL'].iloc[-1]).any()
        if(df['SMA'].iloc[-1] > df['LMA'].iloc[-1]).any()  and pos == 0:
            BuyCondition = True
    
        #CONDITION - SELL
        #and (df['MACD'].iloc[-1] < df['SL'].iloc[-1]).any()
        if (df['SMA'].iloc[-1] < df['LMA'].iloc[-1]).any()  and pos == 0:
            SellCondition = True
    
        #CONDITION - CLOSE BUY
        #and (df['MACD'].iloc[-1] < df['SL'].iloc[-1]).any()
        if (df['SMA'].iloc[-1] < df['LMA'].iloc[-1]).any()  and pos == 1:
            CloseBuy = True
    
        #CONDITION - CLOSE SELL
        #and (df['MACD'].iloc[-1] < df['SL'].iloc[-1]).any()
        if (df['SMA'].iloc[-1] < df['LMA'].iloc[-1]).any()  and pos == 1:
            CloseSell = True

        #    BUY
        if BuyCondition is not None and BuyCondition == True:
            stopLoss = df['stopLoss'].iloc[-1]
            takeProfit = df['takeProfit'].iloc[-1]
            price = df['Close'].iloc[-1]
            lma = df['LMA'].iloc[-1]
            sma = df['SMA'].iloc[-1]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f' BUY - time: {timestamp}, Close: {price}, MAL: {lma}, MS: {sma}')
            buy()
            pos = 1
            buyOpenPrice = df['Close'].iloc[-1] 
            BuyCondition = False

        #    SELL
        if SellCondition is not None and SellCondition == True :
            price = df['Close'].iloc[-1]
            lma = df['LMA'].iloc[-1]
            sma = df['SMA'].iloc[-1]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f' SELL - time: {timestamp}, Close: {price}, MAL: {lma}, MS: {sma},')
            #sell()
            pos = 2
            sellOpenPrice = df['Close'].iloc[-1]
            SellCondition = False

    #   CONDITION CLOSE BUY   
        if CloseBuy is not None and CloseBuy == True:
            price = df['Close'].iloc[-1]
            lma = df['LMA'].iloc[-1]
            sma = df['SMA'].iloc[-1]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            close()
            ClosePrice = price
            BuyProfit = ((ClosePrice - buyOpenPrice)/ buyOpenPrice)* 100
            print(f'SMA CLOSE ({BuyProfit}) - time: {timestamp}, Close: {price}, MAL: {lma}, MS: {sma}') 
            pos = 0
            lstpos = 1
            profit_save(BuyProfit)
            CloseBuy = False

    #   CONDITION CLOSE SELL  
        if CloseSell is not None and CloseSell == True :
            price = df['Close'].iloc[-1]
            lma = df['LMA'].iloc[-1]
            sma = df['SMA'].iloc[-1]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ClosePrice = price
            SellProfit = "NaN" #((sellOpenPrice - ClosePrice)/ sellOpenPrice)* 100
            print(f'SMA CLOSE ({SellProfit}) - time: {timestamp}, Close: {price}, MAL: {lma}, MS: {sma}') 
            close()
            pos = 0
            lstpos = 2
            profit_save(SellProfit)
            CloseSell = False
    #   OPEN BUY
    # Cprice = df['Close'].iloc[-1]
        if df['SMA'].iloc[-1] > df['LMA'].iloc[-1] and pos == 1:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            price = df['Close'].iloc[-1]
            lma = df['LMA'].iloc[-1]
            sma = df['SMA'].iloc[-1]  
            # stopLoss = stopLoss + ( stopLoss*TSP)
            #takeProfit = takeProfit + ( takeProfit * TTP)
            pos = 1
            print(f'OPEN BUY - time: {timestamp}, Close: {price}, MAL: {lma}, MS: {sma}, stopLoss: {stopLoss}, ')

    #   OPEN SELL
        Cprice = df['Close'].iloc[-1]
        if df['SMA'].iloc[-1] < df['LMA'].iloc[-1] and pos == 2:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            price = df['Close'].iloc[-1]
            lma = df['LMA'].iloc[-1]
            sma = df['SMA'].iloc[-1]  
            #stopLossSELL = stopLossSELL - ( stopLoss*TSP)
            #takeProfitSELL = takeProfitSELL - ( takeProfit * TTP)
            stopLoss = "NaN"
            takeProfit = "NaN"
            pos = 2
            print(f'OPEN SELL - time: {timestamp}, Close: {price}, MAL: {lma}, MS: {sma}, stopLoss: {stopLoss}, ')

    #   NO ACTION
        if pos == 0:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            price = df['Close'].iloc[-1]
            lma = df['LMA'].iloc[-1]
            sma = df['SMA'].iloc[-1]
            print(f'NO ACTION - time: {timestamp}, Close: {price}, MAL: {lma}, MS: {sma}')
            SELL_reentry_condition = 0
            BUY_reentry_condition = 0
            # Re-enter BUY position
            if df['SMA'].iloc[-1] > df['SMA'].iloc[-1] and df['Close'].iloc[-1] >= df["high_of_trend"].iloc[-1]:
                BUY_reentry_condition = 1
                SELL_reentry_condition = 0
            if pos == 0 and BUY_reentry_condition == 1:
                if df['Close'].iloc[-1] >= df['high_of_trend'].iloc[-1]:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    price = df['Close'].iloc[-1]
                    lma = df['LMA'].iloc[-1]
                    sma = df['SMA'].iloc[-1]
                    pos = 1
                    buyOpenPrice = df['Close'].iloc[-1]
                    print(f'RE-ENTER BUY - time: {timestamp}, Close: {price}, MAL: {lma}, MS: {sma}, stopLoss: {stopLoss}')
                    buy()
                    BUY_reentry_condition = 0
        while pos == 1:
            time.sleep(TIME)
            
pos = 0
start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f'START { start_timestamp }')
stpos = 0

while True:
    main(price_json_paths, pos)
    time.sleep(TIME)