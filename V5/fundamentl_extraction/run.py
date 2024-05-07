import requests
from bs4 import BeautifulSoup
import json

one_co_file_path = r'C:\Users\David\Documents\ProfitPilot\V5\fundamentl_extraction\one_co.json'
symbol_list_file_path = r'C:\Users\David\Documents\ProfitPilot\V5\results\TB_nalysed_stocks.json'

print('RUNNING FUNDAMENTAL EXTRACTION')

def clear_file(file_path):
    try:
        with open(file_path, "w") as json_file:
            print('***FILE CEARED***')
    except Exception as e:
        print(f"Error creating the JSON file: {e}")

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

def get_td_content(url):
    td_contents = []  
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        td_tags = soup.find_all('td')
        
        for td in td_tags:
            td_contents.append(td.get_text())

        td_contents_cut = td_contents.copy() 

        index_list = [0,2,3,5,6,8,9,11,12,14,15,17,18,20,21,23,24,26,27,29,30,32,33,35,36,38,39,41,42,44,45,47,48,50,51,53,54,56,57,59,60,62]
        for index in sorted(index_list, reverse=True):
            del td_contents_cut[index]

        return td_contents, td_contents_cut
    else:
        print("Failed to retrieve content from the URL.")
        return None
    
symbol_list = extract_keys_from_json(symbol_list_file_path) 

clear_file(one_co_file_path) 

keys = ['Revenue', 'Operating expense','RevenueNet', 'Net profit margin', 'Earnings per share', 'EBITDAEarnings', 'Effective tax rate', 'Cash and short-term investments', 'Total assets', 'Total liabilities', 'Total equit', 'Shares outstanding', 'Price to book', 'Return on assets', 'Return on capital', 'Net income', 'Cash from operation', 'Cash from investing', 'Cash from financing', 'Net change in cash', 'Free cash flow']
with open(one_co_file_path, "a") as json_file:
    json_file.write('[ ')
    json_file.write('\n')
for symbol in symbol_list:
    url = f"https://www.google.com/finance/quote/{symbol}:NASDAQ" 
    symbol_list = extract_keys_from_json(symbol_list_file_path) 
    td_content_list, cut_list = get_td_content(url)
    if len(cut_list) == len(keys):
        my_dict = dict(zip(keys, cut_list))
        if symbol != symbol_list[-1]:
            with open(one_co_file_path, "a") as json_file:
                json.dump({symbol: my_dict}, json_file)
                json_file.write('\n')
                json_file.write(', ')
        if symbol == symbol_list[-1]:
            with open(one_co_file_path, "a") as json_file:
                json.dump({symbol: my_dict}, json_file)
                json_file.write('\n')
    else:
        print("Lists are of different lengths. Cannot create dictionary.")
        continue
with open(one_co_file_path, "a") as json_file:
    json_file.write(']')

print("Dictionary successfully saved to", one_co_file_path)
