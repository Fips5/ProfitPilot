import json
import subprocess
import pandas as pd
import time
import threading
import os
import multiprocessing

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

xy_file = r'C:\Users\David\Documents\ProfitPilot\V5\XY\find_xy.py'
price_extraction_file = r"C:\Users\David\Documents\ProfitPilot\V5\Live_Price_Analysis\price.py"
price_analysis_file = r"C:\Users\David\Documents\ProfitPilot\V5\Live_Price_Analysis\price_analysis.py"

def extract_live_price():
    subprocess.run(['python', price_extraction_file])
def analyse_live_price():
    subprocess.run(['python', price_analysis_file])


symbol_list_json_path = r'C:\Users\David\Documents\ProfitPilot\V5\results\TB_nalysed_stocks.json'
symbol_list = extract_keys_from_json(symbol_list_json_path)

premarket_python_file_path = r'C:\Users\David\Documents\ProfitPilot\V5\Premarket\premarket.py'

subprocess.run(['python', premarket_python_file_path])

def continue_analysis():
    while True:
        user_input = input("Do you want to continue live analysis? (y/n): ").lower()
        if user_input == 'y':
            return True

        elif user_input == 'n':
            return False
        else:
            print("Be serious! Please input 'y' or 'n'.")
            user_input = input("You have 5 seconds to reconsider: ").lower()
            time.sleep(5)
            if user_input not in ['y', 'n']:
                print("You have been warned! Goodbye!")
                break


print('***PREMRKET ANLYSIS DONE***')

# Example usage:
if continue_analysis() == True:
    print("***STARTING LIVE PRICE ANLYSIS")
    subprocess.run(['python', xy_file])
    time.sleep(3)
    
    price_p1 = multiprocessing.Process(target = extract_live_price, args= [])
    price_p2 = multiprocessing.Process(target = analyse_live_price, args= [])

    finish = time.perf_counter()

    if __name__ == '__main__':
        price_p1.start()
        price_p2.start()

    finish = time.perf_counter()
    print("Analysis stopped.", finish)