import json
from PIL import Image
import pytesseract
import pyautogui
import time
from datetime import datetime
import os

TIME = 35
MAX_ENTRIES = 20

coordonates_json_path = r'C:\Users\David\Documents\ProfitPilot\V5\XY\coordinates.json'

def read_coordinates_from_json(filename):
    with open(filename, 'r') as f:
        coordinates = json.load(f)
    return coordinates

print('\n \n \n \n ')
print('BEFORE STARTING LOCATE THE COORDONATES TO GET EXTRACT THE PRICES')
print('\n \n \n \n ')

coordinates_buy = read_coordinates_from_json(coordonates_json_path)

json_paths = [
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_1.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_2.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_3.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_4.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_5.json',
    r'C:\Users\David\Documents\ProfitPilot\V5\json_prices\price_6.json'
]
'''
coordinates_buy = [
    (1047, 259, 1111, 293),     #1
    (1047, 332 , 1111, 357),    #2
    (1047, 389 , 1111, 418),    #3
    (1047, 452 , 1111, 484),    #4
    (1047, 516 , 1111, 547),    #5
    (1047, 580 , 1111, 609),    #6
]
'''
screenshot_paths = [
    r'C:\Users\David\Documents\ProfitPilot\V5\screenshots\screenshot_1.png',
    r'C:\Users\David\Documents\ProfitPilot\V5\screenshots\screenshot_2.png',
    r'C:\Users\David\Documents\ProfitPilot\V5\screenshots\screenshot_3.png',
    r'C:\Users\David\Documents\ProfitPilot\V5\screenshots\screenshot_4.png',
    r'C:\Users\David\Documents\ProfitPilot\V5\screenshots\screenshot_5.png',
    r'C:\Users\David\Documents\ProfitPilot\V5\screenshots\screenshot_6.png'
]

def save_price_to_data(prices, json_paths):
    for price, json_path in zip(prices, json_paths):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"price": price, "timestamp": timestamp}
        
        # Check if file exists and is not empty
        if os.path.isfile(json_path) and os.path.getsize(json_path) > 0:
            try:
                with open(json_path, "r") as file:
                    history_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading JSON from {json_path}: {e}")
                history_data = []
        else:
            history_data = []

        history_data.append(data)

        # Keep only the last MAX_HISTORY_ENTRIES entries
        history_data = history_data[-MAX_ENTRIES:]

        with open(json_path, "w") as file:
            json.dump(history_data, file, indent=2)

def tesseract(coordinates_buy, json_paths):
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    custom_config = r'--psm 6 outputbase digits'

    try:
        price_recall = 1
        while True:
            prices = []
            for i, (coords, path, json_path_tes) in enumerate(zip(coordinates_buy, screenshot_paths, json_paths), 1):
                left, top, right, bottom = coords
                region = (left, top, right - left, bottom - top)  # Calculate region based on coordinates
                screenshot = pyautogui.screenshot(region=region)
                screenshot.save(path)

                #print("Performing OCR...")
                text = pytesseract.image_to_string(screenshot, config=custom_config)
                price = float(text[:-1]) if text else '0'
                prices.append(price)
                #print(price)
            #print(prices)
            save_price_to_data(prices, json_paths)
            time.sleep(TIME)
    except Exception as e:
        print("An error occurred:", e)

n  = 1
Ctime = time.localtime()
Wtime = (50 - Ctime.tm_sec) - n     #
if Wtime < n:
    Wtime = 0
time.sleep(Wtime)
print(f"wait {Wtime} seconds")
while True:
    try:
        tesseract(coordinates_buy, json_paths)
    except Exception as e:
        print('Error', e)
        continue