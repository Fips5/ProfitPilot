import json
import subprocess
import pandas as pd

path_news_extraction = r'C:\Users\David\Documents\ProfitPilot\V5\news_extrction\run.py'
path_fundmental_extraction = r'C:\Users\David\Documents\ProfitPilot\V5\fundamentl_extraction\run.py'
path_news_analysis = r'C:\Users\David\Documents\ProfitPilot\V5\AI_news_anlysis\model.py'
path_fundamental_analysis = r'C:\Users\David\Documents\ProfitPilot\V5\fundamental_analysis\main.py'
path_technical_anlysis = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\2050.py'

subprocess.run(['python', path_news_extraction])
subprocess.run(['python', path_fundmental_extraction])
subprocess.run(['python', path_news_analysis])
subprocess.run(['python', path_fundamental_analysis])
subprocess.run(['python', path_technical_anlysis])

def news_read(json_file_path):
    sentiment_dict = {}
    with open(r'C:\Users\David\Documents\ProfitPilot\V5\AI_news_anlysis\output.json', 'r') as file:
        json_data = json.load(file)

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

news_sentiment_path = r'C:\Users\David\Documents\ProfitPilot\V5\AI_news_anlysis\output.json'
news_sentiment_dict = news_read(news_sentiment_path)

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

one_day_technical_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\1d.json'
one_hour_technical_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\1h.json'
five_days_technical_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\5d.json'
fiveten_min_technical_path = r'C:\Users\David\Documents\ProfitPilot\V5\technical_analisis\15m.json'

one_day_technical_df = technical_read(one_day_technical_path)
one_hour_technical_df = technical_read(one_hour_technical_path)
five_days_technical_df = technical_read(five_days_technical_path)
fiveten_min_technical_df = technical_read(fiveten_min_technical_path)

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

print(fundametal_df)








