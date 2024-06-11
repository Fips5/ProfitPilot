import json
from datetime import datetime
import pyautogui

def extract_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} is not a valid JSON file.")
        return None

def save_json_data(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error: Could not save data to {file_path}. {e}")



def autoclose():
    pyautogui.hotkey('ctrl', '2')   #open new tab

    #pyautogui.moveTo(





def close(symbol):

    autoclose()
    
    open_orders_path = r'C:\Users\David\Documents\ProfitPilot\V5\Live_Price_Analysis\buy_orders.json'
    close_orders_path = r'C:\Users\David\Documents\ProfitPilot\V5\Live_Price_Analysis\close_orders.json'

    open_orders = extract_json_data(open_orders_path)
    if open_orders is None:
        return

    latest_order = None
    for order in open_orders:
        if order['symbol'] == symbol:
            if latest_order is None or order['id'] > latest_order['id']:
                latest_order = order

    if latest_order is None:
        raise ValueError(f"No open order found for symbol: {symbol}")

    # Update the latest order with the current timestamp
    latest_order['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    close_orders = extract_json_data(close_orders_path)
    if close_orders is None:
        close_orders = []

    # Append the latest order to the close orders list
    close_orders.append(latest_order)
    
    # Write the updated close orders to close_orders.json
    save_json_data(close_orders_path, close_orders)

symbol_to_close = 'NFLX'
close(symbol_to_close)
