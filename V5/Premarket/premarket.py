import json
import subprocess
import pandas as pd

def extract_keys_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            keys = list(data.keys())
            return keys
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
        return []
    except json.JSONDecodeError:
        print("Invalid JSON format in the file. Please provide a valid JSON file.")
        return []

symbol_list_json_path = r'C:\Users\David\Documents\ProfitPilot\V5\results\TB_nalysed_stocks.json'
symbol_list = extract_keys_from_json(symbol_list_json_path)


path_news_extraction = r'C:\Users\David\Documents\ProfitPilot\V5\news_extrction\run.py'
path_fundmental_extraction = r'C:\Users\David\Documents\ProfitPilot\V5\fundamentl_extraction\run.py'
path_news_analysis = r'C:\Users\David\Documents\ProfitPilot\V5\AI_news_anlysis\model.py'
path_fundamental_analysis = r'C:\Users\David\Documents\ProfitPilot\V5\fundamental_analysis\main.py'
path_technical_anlysis = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\2050.py'

subprocess.run(['python', path_news_extraction])
subprocess.run(['python', path_news_analysis])

#subprocess.run(['python', path_fundmental_extraction])
#subprocess.run(['python', path_fundamental_analysis])

subprocess.run(['python', path_technical_anlysis])

def news_read(json_file_path):
    sentiment_dict = {}
    
    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
    except json.decoder.JSONDecodeError:
        print("JSON decoding error: File is empty or not in valid JSON format.")
        return sentiment_dict

    for company, articles in json_data.items():
        positive_count = 0
        negative_count = 0
    
        for article in articles.values():
            if article["conclusion"] == "positive":
                positive_count += 1
            elif article["conclusion"] == "negative":
                negative_count += 1

        if positive_count > negative_count:
            sentiment_dict[company] = 1  # Positive predominant
        elif negative_count > positive_count:
            sentiment_dict[company] = 0  # Negative predominant
        else:
            sentiment_dict[company] = 0.5  # Equal positive and negative counts

    return sentiment_dict

def dict_to_dataframe(news_dict):
    try:
        df = pd.DataFrame(list(news_dict.items()), columns=['Symbol', 'News Score'])
        return df
    except Exception as e:
        print(f"Error converting dictionary to DataFrame: {e}")
        return None

news_sentiment_path = r'C:\Users\David\Documents\ProfitPilot\V5\AI_news_anlysis\output.json'
news_sentiment_dict = news_read(news_sentiment_path)

news_df = dict_to_dataframe(news_sentiment_dict)

def technical_read(file_path):
    try:
        # Read JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Initialize lists to store data
        symbols = []
        sma_lma = []
        macd_sl = []
        
        # Extract data from JSON
        for symbol, indicators in data.items():
            symbols.append(symbol)
            sma_lma.append(indicators.get('sma/lma'))
            macd_sl.append(indicators.get('macd/sl'))
        
        # Create DataFrame
        df = pd.DataFrame({
            'Symbol': symbols,
            'SMA/LMA': sma_lma,
            'MACD/SL': macd_sl
        })
        
        return df
    
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

five_days_technical_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\5d.json'
one_day_technical_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\1d.json'
one_hour_technical_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\1h.json'
fiveten_min_technical_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\15m.json'

fiveten_min_technical_df = technical_read(fiveten_min_technical_path)   #1
one_hour_technical_df = technical_read(one_hour_technical_path)         #2
one_day_technical_df = technical_read(one_day_technical_path)           #3
five_days_technical_df = technical_read(five_days_technical_path)       #4

def fundamental_read(file_path):
    try:
        # Read JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Initialize lists to store data
        symbols = []
        financial_data = {key: [] for key in data[0][list(data[0].keys())[0]].keys()}
        
        # Extract data from JSON
        for entry in data:
            symbol = list(entry.keys())[0]
            symbols.append(symbol)
            for metric, value in entry[symbol].items():
                financial_data[metric].append(value)
        
        # Create DataFrame
        df = pd.DataFrame(financial_data)
        df.insert(0, 'Symbol', symbols)
        
        return df
    
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None
    
fundamental_output_path = r'C:\Users\David\Documents\ProfitPilot\V5\fundamentl_extraction\one_co.json'
fundametal_df = fundamental_read(fundamental_output_path)

interval_decision_list = [1, 2, 3, 4]
intreval_weight_list = [1, 1, 0.5, 0.5]

general_df = pd.merge(one_hour_technical_df, news_df, on='Symbol')

general_df['Score'] = general_df['SMA/LMA'] + general_df['MACD/SL'] + general_df['News Score']
general_df_sorted = general_df.sort_values(by='Score', ascending=False)

top_6_symbols = general_df_sorted.head(6)
top_6_symbols.reset_index(drop=True, inplace=True)

print(f'*** TOP RESULTS*** \n {top_6_symbols}')

top_symbols_list = top_6_symbols['Symbol'].tolist()

def output_results_data(results_list, json_file_path):
    try:
        data = {"output": results_list}
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file)
        
        print("Updated JSON file with results list.")

    except FileNotFoundError:
        print("File not found at the specified path.")


resuts_file_path = r'C:\Users\David\Documents\ProfitPilot\V5\Premarket_Results\output.json'
print(f'****RESULTS****\n{top_symbols_list}')
output_results_data(top_symbols_list, resuts_file_path)



'''
print(f'FUNDAMENTAL_DF: {fundametal_df.columns}')

print(f'TECHNICAL: {one_hour_technical_df.columns}')

print(f'NEWS DF: {news_df.columns}')

print(general_df)

['NVDA', 'TSLA', 'GOOG', 'META', 'MSFT', 'NFLX']
FUNDAMENTAL_DF: Index(['Symbol', 'Revenue', 'Operating expense', 'RevenueNet',
       'Net profit margin', 'Earnings per share', 'EBITDAEarnings',
       'Effective tax rate', 'Cash and short-term investments', 'Total assets',
       'Total liabilities', 'Total equit', 'Shares outstanding',
       'Price to book', 'Return on assets', 'Return on capital', 'Net income',
       'Cash from operation', 'Cash from investing', 'Cash from financing',
       'Net change in cash', 'Free cash flow'],
      dtype='object')
TECHNICAL: Index(['Symbol', 'SMA/LMA', 'MACD/SL'], dtype='object')
NEWS DICT: {'NVDA': 0.5, 'TSLA': 0.5, 'GOOG': 1, 'META': 0.5, 'MSFT': 1, 'NFLX': 0.5}

  Symbol  SMA/LMA  MACD/SL  News Score
0   NVDA        1        0         0.5
1   TSLA        0        0         0.5
2   GOOG        1        1         1.0
3   META        1        0         0.5
4   MSFT        1        0         1.0
5   NFLX        1        0         0.5

'''
