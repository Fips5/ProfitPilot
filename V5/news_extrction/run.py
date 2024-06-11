import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

print('RUNNING NEWS EXTRACTION')

# Replace "YOUR_NEWS_API_KEY_HERE" with your actual News API key
NEWS_API_KEY = ['97e77dd430f345aab9c79c30c34604b9', '6f1dc9d98c374fb5b923b219e0d82a51', '2b5d8c7991e64d3788482e65196ef314' ]
#'1244e700ddc541ca8f1090038d64de82'
full_stock_list_path = r"C:\Users\David\Documents\ProfitPilot\V5\results\TB_nalysed_stocks.json"
def clear_file(file_path):
    try:
        with open(file_path, "w") as json_file:
            print('***FILE CEARED***')
    except Exception as e:
        print(f"Error creating the JSON file: {e}")

def extract_names(json_file_path):
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        return list(data.keys())

def extract_symbols(json_file_path):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            key_content_list = []
            for key, value in data.items():
                key_content_list.append(value)
            return key_content_list
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {json_file_path}")
        return None
    
def get_news_raw_data(subject, origin_date, API_KEY):
    main_url = f'https://newsapi.org/v2/everything?q={subject}&from={origin_date}&sortBy=popularity&apiKey={API_KEY}'
    news = requests.get(main_url).json()
    
    if 'articles' not in list(news.keys()):
        print("CHNGE API KEY INDEX. PROGRAM STOPPING")
        exit() 

    articles = news['articles']
    df = pd.DataFrame(articles)
    return df

def extract_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    p_tags = soup.find_all('p')
    content = ' '.join([p.get_text(strip=True) for p in p_tags])
    return content

def get_news_articles(ticker, key):
    # Define the base URL and parameters for the News API
    origin_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    df = get_news_raw_data(ticker, origin_date, key)
    
    yahoo_finance_articles = df[df['url'].str.contains('finance.yahoo.com')]
    yahoo_finance_urls = yahoo_finance_articles['url'].tolist()
    
    article_contents = {}
    for url in yahoo_finance_urls:
        content = extract_content(url)
        article_contents[url] = content
    
    return article_contents  # Add this line to return the article_contents dictionary


def get_news_for_tickers(tickers, key):
    news_data = {}
    for ticker in tickers:
        news_data[ticker] = get_news_articles(ticker, key)
    return news_data

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

clear_file(R'C:\Users\David\Documents\ProfitPilot\V5\news_extrction\output.json')

tickers = extract_names(full_stock_list_path)
comp_names =  extract_symbols(full_stock_list_path)
# Get news articles 

ticker_news = get_news_for_tickers(tickers, key = NEWS_API_KEY[2])

# Save 
output_path = r'C:\Users\David\Documents\ProfitPilot\V5\news_extrction\output.json'
save_to_json(ticker_news, output_path)
