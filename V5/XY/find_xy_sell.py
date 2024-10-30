import pyautogui
import json

print('\n \n ')
print('BEFORE STARTING LOCATE THE COORDONATES TO EXECUTE ORDERS AND EXTRACT PRICES:')
print('\n ')
print('SELL COORDONATE \n \n')
coordonates_path = 'XY\coordinates_sell.json'

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

def calculate_center_coordinates(segments):
    centers = []
    for segment in segments:
        xA, yA, xB, yB = segment
        xC = (xA + xB) / 2
        yC = (yA + yB) / 2
        centers.append([xC, yC])
    return centers

centers = calculate_center_coordinates(coordinates_buy)

def save_centers(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")
    
centers_json_path = r'C:\Users\David\Documents\ProfitPilot\V5\XY\centers_sell.json'

save_centers(centers, centers_json_path)