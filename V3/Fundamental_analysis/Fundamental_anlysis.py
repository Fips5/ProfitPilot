import datetime
import pandas as pd
import numpy as np
import json
import requests
from datetime import datetime
import yfinance as yf     #pip install yfinance
import openpyxl
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from transformers import pipeline
import re

#API_KEYSSSSSS
API_KEY ='25fd8be16139b0940d165572b1155730' #25fd8be16139b0940d165572b1155730 #pV7EpV25UlOaPEsj6iWW9sAKTSMtz41I #e25f718f96d02a5416ec26108cbfac8c

NEWS_API_KEY = '1244e700ddc541ca8f1090038d64de82'
NEWS_AI_API_KEY = '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'

ANALYSIS_RESULTS_PATH = r'C:\Users\David\Desktop\Fundamental_analysis\Anlysis_result.xlsx'

results_json_path = r'C:\Users\David\Desktop\Fundamental_analysis\analysis_result.json'

finviz_url = 'https://finviz.com/quote.ashx?t='


#symbol = 'nvda'

#Must hve tickers
check_tickers = ['NVDA', 'AMZN', 'GOOG', 'AMD', 'TSLA', 'MSFT', 'META']

period = 'annual'

number_of_stocks_analysed = 50
# THE FUNCTIONS

def get_market_cap(ticker):
    # Retrieve data
    data = yf.Ticker(ticker)

    # Get market capitalization
    market_cap = data.info['marketCap']

    return market_cap


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
    if json_data is None:
        print("No data received from API.")
        return None
    elif isinstance(json_data, list):
        if len(json_data) == 0:
            print("Received empty list from API.")
            return None
        keys = extract_unique_keys(json_data)
        df = pd.DataFrame(json_data, columns=keys)
        return df
    else:
        print("Expected JSON data, but received:", json_data)
        return None


def get_yf_data(symbol, nr_of_days):

    stock_data = yf.download(symbol, period=f'{nr_of_days}d')

    stock_prices = stock_data['Close']
    stock_dates = stock_prices.index

    df = pd.DataFrame({'Date': stock_dates, 'Price': stock_prices})

    return df

def year_df(date_string):
  try:
        date_object = datetime.strptime(date_string, '%Y-%m-%d')
        year = date_object.year
        return year
  except ValueError as e:
        print("Error:", e)
        return None

def get_data(
        symbol, #AAPL, aapl
        period, #annual
        API_KEY #the api key
):
  #URLS
  income_url =  (f'https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period={period}&apikey={API_KEY}')
  balance_sheet_url =  (f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?period={period}&apikey={API_KEY}")
  key_metrics_url =  (f"https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?period={period}&apikey={API_KEY}")

  #PATHS
  annual_raport_path = r'C:\Users\David\Desktop\Fundamental_analysis\annual.xlsx'
  quarterly_raport_path = r'C:\Users\David\Desktop\Fundamental_analysis\quarterly.xlsx'
  balance_sheet_path = r'C:\Users\David\Desktop\Fundamental_analysis\balance_sheet.xlsx'
  income_path = r'C:\Users\David\Desktop\Fundamental_analysis\income.xlsx'
  key_metrics_path = r'C:\Users\David\Desktop\Fundamental_analysis\key_metrics.xlsx'

  balance_sheet_df = json_to_df(balance_sheet_url)
  income_df = json_to_df(income_url)
  key_metrics_df = json_to_df(key_metrics_url)

  #df.to_excel(key_metrics_url)
  #df.to_excel(the_url2) 
  #df.to_excel(balance_sheet_path)
    # Get the minimum length among the DataFrames
  min_length = min(len(balance_sheet_df), len(income_df), len(key_metrics_df))

    # Trim all DataFrames to the minimum length
  balance_sheet_df = balance_sheet_df[:min_length]
  income_df = income_df[:min_length]
  key_metrics_df = key_metrics_df[:min_length]

    #VARIABLES:
  #1. KEY_METRICS VARIABLES
  revenue_per_share = key_metrics_df['revenuePerShare'].tolist()
  enterprise_value = key_metrics_df['enterpriseValue'].tolist()
  free_casf_flow_per_share = key_metrics_df['freeCashFlowPerShare'].tolist()
  cash_per_share = key_metrics_df['cashPerShare'].tolist()
  ptb_ratio = key_metrics_df['ptbRatio'].tolist()
  payables_turnover = key_metrics_df['payablesTurnover'].tolist()
  free_cash_flow_yield = key_metrics_df['freeCashFlowYield'].tolist()
  invested_capital = key_metrics_df['investedCapital'].tolist()
  debt_to_assets = key_metrics_df['debtToAssets'].tolist()
  days_sales_outstanding = key_metrics_df['daysSalesOutstanding'].tolist()
  net_income_per_share = key_metrics_df['netIncomePerShare'].tolist()
  pe_ratio = key_metrics_df['peRatio'].tolist()
  earnings_yield = key_metrics_df['earningsYield'].tolist()
  market_cap = key_metrics_df['marketCap'].tolist()
  roe = key_metrics_df['roe'].tolist()
  book_value_per_share = key_metrics_df['bookValuePerShare'].tolist()
  price_to_sales_ratio = key_metrics_df['priceToSalesRatio'].tolist()

  #2.BLANCE SHEET VARIABLES:
  long_term_investments = balance_sheet_df['longTermInvestments'].tolist()
  total_current_liabilities = balance_sheet_df['totalCurrentLiabilities'].tolist()
  net_debt = balance_sheet_df['netDebt'].tolist()
  total_equity = balance_sheet_df['totalEquity'].tolist()
  total_liabilities_and_stock_holders_equity = balance_sheet_df['totalLiabilitiesAndStockholdersEquity'].tolist()
  total_liabilities_and_total_equity = balance_sheet_df['totalLiabilitiesAndTotalEquity'].tolist()
  total_liabilities = balance_sheet_df['totalLiabilities'].tolist()
  total_current_asstes = balance_sheet_df['totalCurrentAssets'].tolist()
  total_debt = balance_sheet_df['totalDebt'].tolist()
  goodwill = balance_sheet_df['goodwill'].tolist()
  total_stock_holders_equity = balance_sheet_df['totalStockholdersEquity'].tolist()
  short_term_investments = balance_sheet_df['shortTermInvestments'].tolist()
  total_assets = balance_sheet_df['totalAssets'].tolist()
  goodwill_and_intangible_assent = balance_sheet_df['goodwillAndIntangibleAssets'].tolist()
  total_investments = balance_sheet_df['totalInvestments'].tolist()
  defered_revenue = balance_sheet_df['deferredRevenue'].tolist()
  short_term_debt =balance_sheet_df['shortTermDebt'].tolist()
  cash_and_short_term_investments = balance_sheet_df['cashAndShortTermInvestments'].tolist()
  cash_and_cash_equivalents = balance_sheet_df['cashAndCashEquivalents'].tolist()

  #3.INCOME STATEMENT VFARIABLES:
  cost_of_revenue = income_df['costOfRevenue'].tolist()
  eps = income_df['eps'].tolist()
  gross_profit_ratio = income_df['grossProfitRatio'].tolist()
  cost_and_expenses = income_df['costAndExpenses'].tolist()
  operating_expenses = income_df['operatingExpenses'].tolist()
  operating_income = income_df['operatingIncome'].tolist()
  net_income_ratio = income_df['netIncomeRatio'].tolist()
  ebitda_ratio = income_df['ebitdaratio'].tolist()
  operating_income_ratio = income_df['operatingIncomeRatio'].tolist()
  net_income = income_df['netIncome'].tolist()
  total_outher_income_expenses_net = income_df['totalOtherIncomeExpensesNet'].tolist()
  gross_profit = income_df['grossProfit'].tolist()
  interest_expense = income_df['interestExpense'].tolist()
  interest_income = income_df['interestIncome'].tolist()
  ebitda = income_df['ebitda'].tolist()
  revenue = income_df['revenue'].tolist()
  selling_general_and_administrative_expenses = income_df['sellingGeneralAndAdministrativeExpenses'].tolist()
  income_tax_expense = income_df['incomeTaxExpense'].tolist()

  return balance_sheet_df, income_df, key_metrics_df, revenue_per_share, enterprise_value, free_casf_flow_per_share, cash_per_share, ptb_ratio, payables_turnover, free_cash_flow_yield, invested_capital, debt_to_assets, days_sales_outstanding, net_income_per_share, pe_ratio, earnings_yield, market_cap, book_value_per_share, roe, price_to_sales_ratio, long_term_investments, total_current_liabilities, net_debt, total_equity, total_liabilities_and_stock_holders_equity, total_liabilities_and_total_equity, total_liabilities, total_current_asstes, total_debt, goodwill, total_stock_holders_equity, short_term_investments, total_assets, goodwill_and_intangible_assent, total_investments, defered_revenue, short_term_debt, cash_and_short_term_investments, cash_and_cash_equivalents, cost_of_revenue, eps, gross_profit_ratio, cost_and_expenses, operating_expenses, operating_income, net_income_ratio, ebitda_ratio, operating_income_ratio, net_income, total_outher_income_expenses_net, gross_profit, interest_expense, interest_income, ebitda, revenue, selling_general_and_administrative_expenses, income_tax_expense

def get_news_raw_data(subject, origin_date, API_KEY): #exmple df = get_news_raw_data(symbol, date, API_KEY)
   main_url = f'https://newsapi.org/v2/everything?q={subject}&from={origin_date}&sortBy=popularity&apiKey={API_KEY}'
   news = requests.get(main_url).json()
   articles = news['articles']
   df = pd.DataFrame(articles)
   news = pd.DataFrame(df[['publishedAt', 'title', 'description', 'url']])
   return news

def finviz_news_raw_data(tickers):
    finviz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}
    parsed_data = []

    for ticker in tickers:
        url = finviz_url + ticker
        print("Fetching data for ticker:", ticker)
        try:
            req = Request(url=url, headers={'user-agent': 'my-app'})
            response = urlopen(req)
        except Exception as e:
            print("Error fetching data for ticker", ticker, ":", e)
            continue

        html = BeautifulSoup(response, features='html.parser')
        news_table = html.find(id='news-table')
        if news_table:
            news_tables[ticker] = news_table
        else:
            print("No news table found for ticker:", ticker)

    for ticker, news_table in news_tables.items():
        for row in news_table.findAll('tr'):
            if row.a:  # Check if the <a> tag exists
                title = row.a.text.strip()  # Clean up title: remove leading/trailing whitespaces
            else:
                title = ""  # If <a> tag doesn't exist, assign an empty string to title

            date_data = row.td.text.strip().split(' ')

            if len(date_data) == 1:
                time = date_data[0]  # Assuming it's in 'Today' format
                date = None
            else:
                # Extract the date and time separately
                date = date_data[0]
                time = date_data[1]

                # Convert the date to 'Month-Year' format if it matches the 'Today' format
                if date.startswith('Today'):
                    today = datetime.today()
                    month_year_format_date = today.strftime('%b-%d-%y')
                    date = month_year_format_date

                # If the date is in the 'Month-Year' format, remove additional whitespaces
                elif re.match(r'^\w{3}-\d{2}-\d{2}$', date):
                    date = date.strip()

            parsed_data.append([ticker, date, time, title])

    df = pd.DataFrame(parsed_data, columns=['Ticker', 'Date', 'Time', 'Article'])
    return df

def analyze_sentiment(df):
    # Load sentiment analysis model with specified name and revision
    sentiment_analysis = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", revision="af0f99b")

    # Function to get sentiment analysis result
    def get_sentiment(text):
        result = sentiment_analysis(text)
        label = result[0]['label']
        return label

    # Apply sentiment analysis to each article and create a new column
    df['Sentiment_Label'] = df['Article'].apply(get_sentiment)

    # Function to map sentiment labels to numerical values
    def map_sentiment(sentiment):
        if sentiment == 'NEGATIVE':
            return -1
        elif sentiment == 'NEUTRAL':
            return 0
        elif sentiment == 'POSITIVE':
            return 1
        else:
            return None

    # Map sentiment labels to numerical values and create a new column
    df['Sentiment_Value'] = df['Sentiment_Label'].apply(map_sentiment)

    # Function to calculate median and majority sentiment
    def get_sentiment_stats(df):
        median_sentiment = df['Sentiment_Value'].median()
        majority_sentiment = df['Sentiment_Value'].mode().iloc[0]
        return median_sentiment, majority_sentiment

    # Call the function to get sentiment statistics
    median_sentiment, majority_sentiment = get_sentiment_stats(df)

    return median_sentiment, majority_sentiment, df

def calculate_sentiment_label(df):
    # Step 1: Group by "Ticker" and calculate average sentiment value
    average_sentiments = df.groupby('Ticker')['Sentiment_Value'].mean()

    # Step 2: Determine sentiment label based on average sentiment value
    sentiment_labels = average_sentiments.apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))

    # Step 3: Create a new DataFrame with "Ticker" and "Sentiment_Label"
    new_df = pd.DataFrame({'Ticker': sentiment_labels.index, 'Sentiment_Label': sentiment_labels.values})

    return new_df

def get_market_cap(ticker):
    try:
        data = yf.Ticker(ticker)
        market_cap = data.info.get('marketCap')
        if market_cap is None:
            return 0
        return market_cap
    except Exception as e:
        print(f"Error fetching market cap for {ticker}: {e}")
        return 0


def get_one_day_difference(ticker):
    data = yf.download(ticker, start='2024-03-01', end='2024-03-15')
    if len(data) < 2:
        return None
    one_day_diff = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    one_day_diff_percent = (one_day_diff / data['Close'].iloc[-2]) * 100
    return one_day_diff_percent

def top_n_tickers(n, sort_by='mc'):
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    symbols_sectors_df = df[['Symbol', 'GICS Sector']]
    symbol_list = list(symbols_sectors_df['Symbol'][:n])
    sectors_list = list(symbols_sectors_df['GICS Sector'][:n])
    market_cap_list = []
    one_day_dif_list = []
    for ticker in symbol_list:
        market_cap = get_market_cap(ticker)
        market_cap_list.append(market_cap)
        one_day_diff = get_one_day_difference(ticker)
        one_day_dif_list.append(one_day_diff)

    if sort_by == 'mc':
        sorted_tickers = [x for _, x in sorted(zip(market_cap_list, symbol_list), reverse=True)]
        sorted_market_caps = sorted(market_cap_list, reverse=True)
        top_n_values = sorted_market_caps[:n]
    elif sort_by == 'odf':
        sorted_tickers = [x for _, x in sorted(zip(one_day_dif_list, symbol_list), reverse=True)]
        sorted_one_day_diff = sorted(one_day_dif_list, reverse=True)
        top_n_values = sorted_one_day_diff[:n]
    else:
        print("Invalid sort_by parameter. Please use 'mc' for market cap or 'odf' for one-day difference.")
        return

    #print(f"Sorted Tickers by {sort_by}:", sorted_tickers)
    #print(f"Top {n} {sort_by}: {top_n_values}")
    return sorted_tickers, sectors_list
    #top_n_tickers(5, sort_by='mc')  # Sort by market cap
    #top_n_tickers(5, sort_by='odf')  # Sort by one-day difference

def add_variable_to_metrics(variable_name, values, metrics):
    metrics[variable_name] = values

def check_and_add_tickers(tickers, check_tickers):
    missing_tickers = [ticker for ticker in check_tickers if ticker not in tickers]
    if missing_tickers:
        tickers.extend(missing_tickers)
    return tickers

tickers, sectors = top_n_tickers(number_of_stocks_analysed, sort_by='odf')

tickers = check_and_add_tickers(tickers, check_tickers)

def strategy(tickers, sectors):
  today_date = datetime.today()

  news_data = finviz_news_raw_data(tickers)
  dian_sentiment, majority_sentiment, analyzed_df = analyze_sentiment(news_data)

  sentiment_results_df = calculate_sentiment_label(analyzed_df)
  tickers_1 = sentiment_results_df[sentiment_results_df['Sentiment_Label'] == 1]['Ticker'].tolist()

  strategy_results = []

  for symbol in sentiment_results_df['Ticker'].tolist():
    score = 0
    balance_sheet_df, income_df, key_metrics_df, revenue_per_share, enterprise_value, free_casf_flow_per_share, cash_per_share, ptb_ratio, payables_turnover, free_cash_flow_yield, invested_capital, debt_to_assets, days_sales_outstanding, net_income_per_share, pe_ratio, earnings_yield, market_cap, book_value_per_share, roe, price_to_sales_ratio, long_term_investments, total_current_liabilities, net_debt, total_equity, total_liabilities_and_stock_holders_equity, total_liabilities_and_total_equity, total_liabilities, total_current_asstes, total_debt, goodwill, total_stock_holders_equity, short_term_investments, total_assets, goodwill_and_intangible_assent, total_investments, defered_revenue, short_term_debt, cash_and_short_term_investments, cash_and_cash_equivalents, cost_of_revenue, eps, gross_profit_ratio, cost_and_expenses, operating_expenses, operating_income, net_income_ratio, ebitda_ratio, operating_income_ratio, net_income, total_outher_income_expenses_net, gross_profit, interest_expense, interest_income, ebitda, revenue, selling_general_and_administrative_expenses, income_tax_expense = get_data(symbol, period, API_KEY)

    mas = 6
    mal = 20

    yf_price_df = get_yf_data(symbol, 100)
    end_day_price = get_yf_data(symbol, 5)['Price'].iloc[-1]

  #YF DATA NLYSIS BASED ON QUANT
    yf_price_df['MA_L'] = yf_price_df['Price'].rolling(window=mal).mean()
    yf_price_df['MA_S'] = yf_price_df['Price'].rolling(window=mas).mean()

    if yf_price_df['MA_S'].iloc[-1] > yf_price_df['MA_L'].iloc[-1]:
      ma20_greater_dates = yf_price_df[yf_price_df['MA_S'] > yf_price_df['MA_L']]['Date'].tolist()
      closest_date = min(ma20_greater_dates, key=lambda x: abs(x - today_date))
      trend_change_days = (closest_date - today_date).days
      score += 10
    if yf_price_df['MA_S'].iloc[-1] < yf_price_df['MA_L'].iloc[-1]:
      ma20_greater_dates = yf_price_df[yf_price_df['MA_S'] < yf_price_df['MA_L']]['Date'].tolist()
      closest_date = min(ma20_greater_dates, key=lambda x: abs(x - today_date))
      trend_change_days = (closest_date - today_date).days * -1
      score -= 10
    # trend_change_days > 0 it is  up trend, it is also the number of dys singe the trend chnge it is is <0 t is negtve a down trend

    #Fundamentl nalysis:

    #Price to Book ratio:
    average_ptb_ratio = sum(ptb_ratio) / len(ptb_ratio)
    if ptb_ratio[0] > average_ptb_ratio:
      score = score + 1
    if ptb_ratio[0] < average_ptb_ratio:
      score = score - 1.5

    #Price to Ernings ratio:
    average_pe_ratio = sum(pe_ratio) / len(pe_ratio)
    if pe_ratio[0] > average_pe_ratio:
      score = score + 1
    if pe_ratio[0] < average_pe_ratio:
      score = score - 1.5

    #Price to Ernings to Growth:
    net_income_latest = net_income[0]
    net_income_previous = net_income[1]
    earnings_growth_rate = ((net_income_latest - net_income_previous) / net_income_previous) * 100
    if earnings_growth_rate < 1:
      score = score + 0.5
    if earnings_growth_rate > 1:
      score = score - 0.5

    #Debt to Assets ratio:
    if debt_to_assets[0] > 0:
      score = score + 1
    if debt_to_assets[0] < 0:
      score = score - 1

    #Total Assets
    total_assets_latest = total_assets[0]
    average_total_assets = sum(total_assets)/len(total_assets)

    if average_total_assets > total_assets_latest:
      score = score + 1
    if average_total_assets < total_assets_latest:
      score = score - 1

    #Stock Holders Equity
    total_total_stock_holders_equity_latest = total_stock_holders_equity[0]
    average_total_stock_holders_equity = sum(total_stock_holders_equity)/len(total_stock_holders_equity)

    if average_total_stock_holders_equity > total_total_stock_holders_equity_latest:
      score = score + 1
    if average_total_stock_holders_equity < total_total_stock_holders_equity_latest:
      score = score - 2

    #Revenue & sales:
    revenue_latest = revenue[0]
    average_revenue = sum(revenue) / len(revenue)

    if revenue[1] > revenue_latest:
        score += 1
    if revenue[1] < revenue_latest:
        score -= 2

    #Gross Profit
    gross_profit_latest = gross_profit[0]
    average_gross_profit = sum(gross_profit) / len(gross_profit)

    if average_gross_profit > gross_profit_latest and gross_profit_latest > revenue_latest:
        score += 1
    '''
    if average_gross_profit < gross_profit_latest or (gross_profit_latest < revenue_latest and not (average_gross_profit < gross_profit_latest and gross_profit_latest < revenue_latest)):
        score -= 0.5
    '''
    if average_gross_profit < gross_profit_latest and gross_profit_latest < revenue_latest:
        score -= 1

    #Revenue Growth Rate
    revenue_current = revenue[0]
    revenue_previous = revenue[1]
    revenue_growth_rate = ((revenue_current - revenue_previous) / revenue_previous) * 100

    if revenue_growth_rate > 10:
      score += 1

    if revenue_growth_rate < 10:
      score -= 1

    #Profitability:

    if net_income[0] > 0 :
      score += 1/3
    if gross_profit[0] > 0 :
      score += 1/3
    if operating_income[0] > 0:
      score += 1/3

    if net_income[0] < 0 :
      score -= 1/3
    if gross_profit[0] < 0 :
      score -= 1/3
    if operating_income[0] < 0:
      score -= 1/3

    # Calculate the growth rate of revenue
    expenses_growth_rate = ((cost_and_expenses[0] - cost_and_expenses[1]) / cost_and_expenses[1]) * 100
    revenue_growth_rate = ((revenue[0] - revenue[1]) / revenue[1]) * 100

    if  revenue_growth_rate < expenses_growth_rate :
      score -= 1
    if revenue_growth_rate > expenses_growth_rate:
      score += 1

    strategy_results.append(score)
    #print(f'{symbol} : {score} pts')
  #print(tickers)
  strategy_results.reverse()
  #print(strategy_results)
  min_length = min(len(tickers), len(sectors), len(strategy_results))

  # Trim all lists to the minimum length
  tickers = tickers[:min_length]
  sectors = sectors[:min_length]
  strategy_results = strategy_results[:min_length]
  data = {'Symbol': tickers, 'Sector': sectors, 'Score': strategy_results}
  df = pd.DataFrame(data)
  return df
min_length = min(len(tickers), len(sectors))
tickers = tickers[:min_length]
sectors = sectors[::-1]
sectors = sectors[:min_length]
results = strategy(tickers, sectors)
results_save_one = results
results_save_two = results

def summarize_scores(df):
    idx_max = df.groupby('Sector')['Score'].idxmax()
    idx_min = df.groupby('Sector')['Score'].idxmin()

    symbol_high = df.loc[idx_max, 'Symbol'].values
    symbol_low = df.loc[idx_min, 'Symbol'].values

    summary_df = df.groupby('Sector').agg({
        'Score': ['max', 'min', 'mean'],  # 
    }).reset_index()

    summary_df['Highest Score Symbol'] = symbol_high
    summary_df['Lowest Score Symbol'] = symbol_low

    summary_df.columns = ['Sector', 'Highest Score', 'Lowest Score', 'Average Score', 'Highest Score Symbol', 'Lowest Score Symbol']

    for index, row in summary_df.iterrows():
        if row['Highest Score Symbol'] == row['Lowest Score Symbol']:
            if row['Lowest Score'] == row['Highest Score'] and row['Highest Score'] > 0:
                summary_df.at[index, 'Lowest Score'] = 0
            elif row['Highest Score'] < 0:
                summary_df.at[index, 'Highest Score'] = 0

    return summary_df

out_df = summarize_scores(results)
out_df.to_excel(ANALYSIS_RESULTS_PATH, index = False)

results_list_for_json = (out_df['Highest Score Symbol'].tolist()) + check_tickers
results_dict = {'results': results_list_for_json}

with open(results_json_path, "w") as json_file:
    json.dump(results_dict, json_file)

print('THE CODE WAS EXECUTED AS INTENDED HOPEFULLY')
