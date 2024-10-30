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
coordonadea_sell_file_path = r'C:\Users\David\Documents\ProfitPilot\V5\XY\find_xy_sell.py'


def extract_live_price():
    subprocess.run(['python', coordonadea_sell_file_path])
def extract_live_price():
    subprocess.run(['python', price_extraction_file])
def analyse_live_price():
    subprocess.run(['python', price_analysis_file])


symbol_list_json_path = r'C:\Users\David\Documents\ProfitPilot\V5\results\TB_nalysed_stocks.json'
symbol_list = extract_keys_from_json(symbol_list_json_path)

premarket_python_file_path = r'C:\Users\David\Documents\ProfitPilot\V5\Premarket\premarket.py'

with open('run_check.json', 'r') as json_file:
    mo = json.load(json_file)
    m = mo["running"]

if m != 1:
    subprocess.run(['python', premarket_python_file_path], shell=True)


def continue_analysis():
    user_input = input("Do you want to continue live analysis? (y/n): ").lower()
    if user_input == 'y':
            n = True
            return n

    elif user_input == 'n':
            n = True
            return n
    else:
        print("Be serious! Please input 'y' or 'n'.")
        user_input = input("You have 5 seconds to reconsider: ").lower()
        time.sleep(5)
        if user_input not in ['y', 'n']:
            print("You have been warned! Goodbye!")

if m != 1:
    continue_condition = continue_analysis()
    continue_condition = True

if m == 1:
    print('STOPING PROGRAM')
    time.sleep(10)
    continue_condition = False

# Example usage:
if continue_condition == True and m != 1:
    print('***PREMRKET ANLYSIS DONE***')
    print("***STARTING LIVE PRICE ANLYSIS***")
    subprocess.run(['python', xy_file])
    time.sleep(3)
    
    price_p1 = multiprocessing.Process(target = extract_live_price, args= [])

    finish = time.perf_counter()

    if __name__ == '__main__':
        price_p1.start()
    
    run_check = 1
    data_to_upload = {"running": run_check}
    with open('run_check.json', 'w') as json_file:
        json.dump(data_to_upload, json_file)

    subprocess.run(['python', price_analysis_file])
    finish = time.perf_counter()
    continue_condition = False
    print("Analysis stopped.", finish)