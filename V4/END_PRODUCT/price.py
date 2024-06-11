import json
from PIL import Image
import pytesseract
import pyautogui
import time
from datetime import datetime
TIME = 35
MAX_HISTORY_ENTRIES = 80


def save_price_to_history(price):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"price": price, "timestamp": timestamp}
    try:
        with open(r"C:\Users\David\Desktop\Pilot\END_PRODUCT\history.json", "r") as file:
            history_data = json.load(file)
    except FileNotFoundError:
        history_data = []
    # Append
    history_data.append(data)
    with open("history.json", "w") as file:
        json.dump(history_data, file, indent=2)

def save_price_to_data(price):
    json_file = r'C:\Users\David\Desktop\Pilot\END_PRODUCT\data.json'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"price": price, "timestamp": timestamp}
    
    try:
        with open(json_file, "r") as file:
            history_data = json.load(file)
    except FileNotFoundError:
        history_data = []

    history_data.append(data)

    # Keep only the last MAX_HISTORY_ENTRIES entries
    history_data = history_data[-MAX_HISTORY_ENTRIES:]

    with open(json_file, "w") as file:
        json.dump(history_data, file, indent=2)

def tesseract():
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    custom_config = r'--psm 6 outputbase digits'

    try:
        price_recall = 1
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f" {timestamp} Capturing screenshot...")

            screenshot = pyautogui.screenshot()

            left, top, right, bottom = 174, 125, 270, 156
            cropped_screenshot = screenshot.crop((left, top, right, bottom))

            cropped_screenshot.save('screenshot.png')

            print("Performing OCR...")
            text = pytesseract.image_to_string(cropped_screenshot, config=custom_config)
            price = float(text[:-1]) if text else None

            if price is not None:
                final_price = price 
                print("price:", final_price)
                output_data = {"price": final_price}

                with open('output.json', 'w') as json_file:
                    json.dump(output_data, json_file)
                save_price_to_data(price)
                save_price_to_history(price)

                if price == price_recall:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    print(f" {timestamp} Capturing screenshot AGAIN...")
                    screenshot = pyautogui.screenshot()

                    cropped_screenshot = screenshot.crop((left, top, right, bottom))
                    cropped_screenshot.save('screenshot.png')

                    print("Performing OCR AGAIN...")
                    text = pytesseract.image_to_string(cropped_screenshot, config=custom_config)
                    price = float(text[:-1]) if text else None
            
            price_recall = price
            time.sleep(TIME)
    except Exception as e:
        print("An error occurred:", e)

n  = 1
Ctime = time.localtime()
Wtime = (50 - Ctime.tm_sec) - n #if you he  god py use 60 insted of 50
if Wtime < n:
    Wtime = 0
time.sleep(Wtime)
print(f"wait {Wtime} seconds")
while True:
    try:
        tesseract()
    except Exception as e:
        print('Error', e)
        continue