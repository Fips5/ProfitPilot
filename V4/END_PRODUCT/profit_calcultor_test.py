def calculate_sum(numbers):
    unique_numbers = set()
    total_sum = 0.0

    for num in numbers:
        if num not in unique_numbers:
            total_sum += num
            unique_numbers.add(num)

    return total_sum

def main():
    file_path = r'C:\Users\David\Desktop\Pilot\END_PRODUCT\proft_test.txt'  # Replace with the actual path to your txt file
    with open(file_path, 'r') as file:
        content = file.read()

    # Filter out non-numeric elements and convert the rest to floats
    numbers = [float(num) for num in content.split() if num.replace('.', '', 1).isdigit()]

    result = calculate_sum(numbers)

    print("The sum is:", result)

if __name__ == "__main__":
    main()
