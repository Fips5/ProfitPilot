import pyautogui
import time
import json
SP = 0.002
TP = 0.004
def buy():
    pyautogui.moveTo(967, 302, duration=1)
    pyautogui.click()
    
    time.sleep(2)
    pyautogui.moveTo(976, 224, duration=2)
    pyautogui.click()

    time.sleep(5)
    pyautogui.moveTo(585, 244, duration=1)
    pyautogui.click()


def tbuy():
    print('BUY')
