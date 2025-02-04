import streamlit as st

def calculate_din(height_ft, height_in, weight_lbs, boot_sole_length, skier_type):
    """
    Calculate the approximate DIN setting based on height, weight, boot sole length, and skier type.
    """
    
    # Convert to metric
    height_cm = (height_ft * 12 + height_in) * 2.54  # Convert feet & inches to cm
    weight_kg = round(weight_lbs * 0.453592)  # Convert lbs to kg (rounded)

    # Skier code mapping
    skier_codes = [
        ((10, 13), "A"), ((14, 17), "B"), ((18, 21), "C"), ((22, 25), "D"),
        ((26, 30), "E"), ((31, 35), "F"), ((36, 41), "G"), ((42, 48), "H"),
        ((49, 57), "I"), ((58, 67), "J"), ((68, 78), "K"), ((79, 94), "L"),
        ((95, 109), "M"), ((110, 125), "N"), ((126, 145), "O"), ((146, 210), "P")
    ]

    # Determine skier code
    skier_code = None
    for (min_weight, max_weight), code in skier_codes:
        if min_weight <= weight_kg <= max_weight:
            skier_code = code
            break
    
    if not skier_code:
        return "Invalid height/weight combination."

    # Adjust for height
    if height_cm <= 148 and skier_code in {"I", "J", "K", "L"}:
        skier_code = chr(ord(skier_code) - 1)  # Move down a row
    elif height_cm >= 194 and skier_code in {"I", "J", "K", "L"}:
        skier_code = chr(ord(skier_code) + 1)  # Move up a row

    # DIN Chart
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
        "J": [5.50, 5.50, 5.00, 4.50, 4.00, 3.50],  # Corrected
        "K": [6.50, 6.50, 6.00, 5.50, 5.00, 4.50],
        "L": [7.50, 7.50, 7.00, 6.50, 6.00, 5.50],
        "M": [8.50, 8.50, 8.50, 8.00, 7.00, 6.50],
        "N": [10.00, 10.00, 10.00, 9.50, 9.00, 8.50],
        "O": [11.50, 11.50, 11.50, 11.00, 10.00, 9.50],
        "P": [13.00, 13.00, 13.00, 13.00, 12.00, 11.50]
    }

    # Boot Sole Length Category
    bsl_categories = [(250, 0), (270, 1), (290, 2), (310, 3), (330, 4)]
    column = next((col for max_bsl, col in bsl_categories if boot_sole_length <= max_bsl), 5)

    base_din = din_chart.get(skier_code, [None])[column]
    if base_din is None:
        return "Could not determine DIN setting."

    # Adjust for skier type (Skier Type 1 stays the same, Type 2 moves up 1 row, Type 3 moves up 2 rows)
    skier_code_list = list(din_chart.keys())
    skier_index = skier_code_list.index(skier_code)

    if skier_type == "2":  # Intermediate skier
        skier_index = min(len(skier_code_list) - 1, skier_index + 1)
    elif skier_type == "3":  # Aggressive skier
        skier_index = min(len(skier_code_list) - 1, skier_index + 2)

    adjusted_din = din_chart[skier_code_list[skier_index]][column]

    return f"Recommended DIN setting: {adjusted_din:.1f}"


# ------------------- STREAMLIT APP -------------------
st.title("🎿 Ski DIN Calculator")

# User inputs
height_ft = st.number_input("Height (feet):", min_value=1, max_value=8, value=5)
height_in = st.number_input("Height (inches):", min_value=0, max_value=11, value=4)
weight_lbs = st.number_input("Weight (lbs):", min_value=20, max_value=300, value=135)
boot_sole_length = st.number_input("Boot Sole Length (mm):", min_value=200, max_value=400, value=297)
skier_type = st.radio("Skier Type:", ["1", "2", "3"], index=1)

# Calculate DIN
if st.button("Calculate DIN"):
    din_result = calculate_din(height_ft, height_in, weight_lbs, boot_sole_length, skier_type)
    st.success(din_result)


