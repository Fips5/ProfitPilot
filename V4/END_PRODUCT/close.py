import pyautogui
import time

def close():
    pyautogui.moveTo(903, 157, duration=1)
    pyautogui.click()

    pyautogui.sleep(1)
    pyautogui.hotkey('ctrl', '2')

    pyautogui.sleep(3)
    pyautogui.moveTo(976, 222, duration=1)
    pyautogui.click()
    pyautogui.sleep(1)
    pyautogui.click()
    pyautogui.sleep(1)
    pyautogui.click()

    #pyautogui.sleep(12.62)
    pyautogui.moveTo(447, 253, duration=0)
    pyautogui.click()

    pyautogui.sleep(0.5)
    pyautogui.moveTo(1272, 339, duration=0)
    pyautogui.click()

    pyautogui.sleep(1)
    pyautogui.moveTo(680, 532, duration=0)
    pyautogui.click()

    pyautogui.hotkey('ctrl', '1')
    pyautogui.sleep(1)
    pyautogui.moveTo(975, 224, duration=1)
    pyautogui.sleep(1)
    pyautogui.click()


def tclose():
    print('CLOSE')
