def calculate_din(height_ft, height_in, weight_lbs, boot_sole_length, skier_type):
    """
    Calculate the approximate DIN setting based on height, weight, boot sole length, and skier type.
    """

    # Convert to metric
    height_cm = (height_ft * 12 + height_in) * 2.54  # Convert feet & inches to cm
    weight_kg = round(weight_lbs * 0.453592)  # Use round() instead of int()

    # Step 1: Determine skier code based on weight and height
    skier_codes = [
        ((10, 13), "A"), ((14, 17), "B"), ((18, 21), "C"), ((22, 25), "D"),
        ((26, 30), "E"), ((31, 35), "F"), ((36, 41), "G"), ((42, 48), "H"),
        ((49, 57), "I"), ((58, 67), "J"), ((68, 78), "K"), ((79, 94), "L"),
        ((95, 109), "M"), ((110, 125), "N"), ((126, 145), "O"), ((146, 210), "P")
    ]
    
    skier_code = None
    for (min_weight, max_weight), code in skier_codes:
        if min_weight <= weight_kg <= max_weight:
            skier_code = code
            break
    
    if not skier_code:
        return "Invalid height/weight combination."

    # Adjust skier code based on height
    if height_cm <= 148 and skier_code in {"I", "J", "K", "L"}:
        skier_code = chr(ord(skier_code) - 1)  # Move down one code
    elif height_cm >= 194 and skier_code in {"I", "J", "K", "L"}:
        skier_code = chr(ord(skier_code) + 1)  # Move up one code

    # Step 2: Map skier code to a base DIN value using boot sole length
    din_chart = {
        "A": [0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
        "B": [1.00, 1.00, 0.75, 1.00, 1.00, 1.00],
        "C": [1.50, 1.25, 1.00, 1.00, 1.00, 1.00],
        "D": [1.75, 1.50, 1.50, 1.25, 1.25, 1.25],
        "E": [2.25, 2.00, 1.75, 1.50, 1.50, 1.50],
        "F": [2.75, 2.50, 2.25, 2.00, 1.75, 1.75],
        "G": [3.50, 3.00, 2.75, 2.50, 2.25, 2.00],
        "H": [3.50, 3.50, 3.00, 3.00, 2.75, 2.50],
        "I": [4.50, 4.50, 4.00, 3.50, 3.50, 3.00],
        "J": [5.50, 5.50, 5.00, 4.50, 4.00, 3.50],  # Adjusted J row
        "K": [6.50, 6.50, 6.00, 5.50, 5.00, 4.50],
        "L": [7.50, 7.50, 7.00, 6.50, 6.00, 5.50],
        "M": [8.50, 8.50, 8.50, 8.00, 7.00, 6.50],
        "N": [10.00, 10.00, 10.00, 9.50, 9.00, 8.50],
        "O": [11.50, 11.50, 11.50, 11.00, 10.00, 9.50],
        "P": [13.00, 13.00, 13.00, 13.00, 12.00, 11.50]
    }

    # Boot Sole Length Category
    if boot_sole_length <= 250:
        column = 0
    elif 251 <= boot_sole_length <= 270:
        column = 1
    elif 271 <= boot_sole_length <= 290:
        column = 2
    elif 291 <= boot_sole_length <= 310:
        column = 3
    elif 331 <= boot_sole_length <=330:
        column = 4
    else:
        column = 5
        

    base_din = din_chart.get(skier_code, [None])[column]
    if base_din is None:
        return "Could not determine DIN setting."

    # Step 3: Adjust for Skier Type (Move up/down a row instead of adding/subtracting numbers)
    skier_code_list = list(din_chart.keys())
    skier_index = skier_code_list.index(skier_code)
    
    if skier_type == "2":  # intermediate skier
        skier_index = min(len(skier_code_list) - 1, skier_index + 1)  # Move up one row
    elif skier_type == "3":  # Aggressive skier
        skier_index = min(len(skier_code_list) - 1, skier_index + 2)  # Move up two rows
    
    adjusted_din = din_chart[skier_code_list[skier_index]][column]

    # Ensure DIN is never below 0.5
    adjusted_din = max(0.5, adjusted_din)

    return f"Recommended DIN setting: {adjusted_din:.1f}"

# Main function using input()
def main():
    print("\n🎿 Welcome to the Ski DIN Calculator! 🎿")

    # Get user input directly using input()
    height_ft = int(input("Enter your height (feet): "))
    height_in = int(input("Enter your height (inches): "))
    weight_lbs = int(input("Enter your weight (lbs): "))
    boot_sole_length = int(input("Enter your boot sole length (mm): "))

    # Validate skier type input
    while True:
        skier_type = input("Enter your skier type (1, 2, 3): ").strip()
        if skier_type in {"1", "2", "3"}:
            break
        print("Invalid input. Please enter '1', '2', or '3'.")

    # Calculate DIN
    din_setting = calculate_din(height_ft, height_in, weight_lbs, boot_sole_length, skier_type)
   
    print("\n⛷️ " + din_setting + " ⛷️")

# Run the program
if __name__ == "__main__":
    main()

