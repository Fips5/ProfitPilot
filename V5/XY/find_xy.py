import pyautogui
import json

print('\n \n \n \n ')
print('BEFORE STARTING LOCATE THE COORDONATES TO GET EXTRACT THE PRICES')
print('\n \n \n \n ')

coordonates_path = 'XY\coordinates.json'

def get_coordinates(num_coords):
    coordinates = []
    for i in range(num_coords):
        input("Move the mouse to the top left corner of square {} and press Enter.".format(i+1))
        x_top_left, y_top_left = pyautogui.position()
        input("Move the mouse to the bottom right corner of square {} and press Enter.".format(i+1))
        x_bottom_right, y_bottom_right = pyautogui.position()
        coordinates.append((x_top_left, y_top_left, x_bottom_right, y_bottom_right))
    return coordinates

coordinates_buy = get_coordinates(6)


def save_coordinates_to_json(coordinates, filename):
    with open(filename, 'w') as f:
        json.dump(coordinates, f)

save_coordinates_to_json(coordinates_buy, coordonates_path)