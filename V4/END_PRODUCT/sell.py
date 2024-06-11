import pyautogui
import time

def sell():
    pyautogui.moveTo(885, 299, duration=1)
    pyautogui.click()
    
    time.sleep(2)
    pyautogui.moveTo(976, 224, duration=2)
    pyautogui.click()

    time.sleep(5)
    pyautogui.moveTo(585, 244, duration=1)
    pyautogui.click()

def tsell():
    print('SELL')
