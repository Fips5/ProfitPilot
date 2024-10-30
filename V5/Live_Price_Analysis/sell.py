import json
import pyautogui
import time
from datetime import datetime
import os

def extract_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON file.")
        return None

def add_order_entry(id, symbol, timestamp):
    file_path = r'C:\Users\David\Documents\ProfitPilot\V5\Live_Price_Analysis\sell_orders.json'
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)
    
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = []
    
    if not isinstance(data, list):
        raise ValueError("JSON file does not contain a list of entries.")
        
    new_entry = {
        "id": id,
        "symbol": symbol,
        "timestamp": timestamp
    }
    data.append(new_entry)
        
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def sell(symbol,list_number):
    centers_json_path_list = r'C:\Users\David\Documents\ProfitPilot\V5\XY\centers_sell.json'
    centers_list = extract_json_data(centers_json_path_list)

    with open(r"C:\Users\David\Documents\ProfitPilot\V5\Live_Price_Analysis\ids.json", 'r') as file:
        id_data = json.load(file)

    current_timestamp = datetime.now()
    timestamp_str = current_timestamp.strftime('%Y-%m-%d %H:%M')

    id = id_data['live_id']

    buy_button_coordonates = centers_list[list_number]
    buy_button_coordonatesX = buy_button_coordonates[0] - 20
    buy_button_coordonatesY = buy_button_coordonates[1]

    pyautogui.moveTo(buy_button_coordonatesX, buy_button_coordonatesY, duration=1)
    pyautogui.click()

    print(f"\nOrder BUY - id: {id}, {symbol} ,{timestamp_str}")

    id_data['live_id'] += 1
    new_id_data = id_data
    with open(r"C:\Users\David\Documents\ProfitPilot\V5\Live_Price_Analysis\ids.json", 'w') as file:
            json.dump( new_id_data , file, indent=4)
    add_order_entry( id, symbol, timestamp_str )
