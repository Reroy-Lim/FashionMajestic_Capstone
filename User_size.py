def get_user_input(prompt, min_val, max_val, decimals=2):
    while True:
        try:
            val = float(input(f"{prompt} (e.g., {'175.5' if decimals == 1 else '75.50'}): "))
            if val < min_val or val > max_val:
                print(f"❌ Please enter a value between {min_val} and {max_val}.")
                continue
            val = round(val, decimals)
            print(f"✅ You entered: {val:.{decimals}f}")
            return val
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def get_age_input(prompt, min_val, max_val):
    while True:
        try:
            val = int(input(f"{prompt} (e.g., 25): "))
            if val < min_val or val > max_val:
                print(f"❌ Please enter an age between {min_val} and {max_val}.")
                continue
            print(f"✅ You entered: {val}")
            return val
        except ValueError:
            print("❌ Invalid input. Please enter a whole number.")

def estimate_base_size(height_cm, weight_kg):
    if height_cm < 165 and weight_kg < 60:
        return "S"
    elif 165 <= height_cm < 175 and 60 <= weight_kg < 75:
        return "M"
    elif 175 <= height_cm < 185 and 75 <= weight_kg < 90:
        return "L"
    else:
        return "XL"

def show_size_range(base_size):
    if base_size == "S":
        sizes = ["XS", "S", "M"]
    elif base_size == "M":
        sizes = ["S", "M", "L"]
    elif base_size == "L":
        sizes = ["M", "L", "XL"]
    elif base_size == "XL":
        sizes = ["L", "XL", "XXL"]
    else:
        sizes = ["S", "M", "L"]
    return sizes

def convert_to_uk_size(category, size_label, gender):
    uk_sizes = {
        "tshirt": {
            "male": {"XS": "UK XXS", "S": "UK S", "M": "UK M", "L": "UK L", "XL": "UK XL", "XXL": "UK XXL"},
            "female": {"XS": "UK 6", "S": "UK 8", "M": "UK 10–12", "L": "UK 14–16", "XL": "UK 18", "XXL": "UK 20+"}
        },
        "pants": {
            "male": {"XS": "UK 26", "S": "UK 28–30", "M": "UK 32–34", "L": "UK 36–38", "XL": "UK 40", "XXL": "UK 42+"},
            "female": {"XS": "UK 6", "S": "UK 8–10", "M": "UK 12–14", "L": "UK 16–18", "XL": "UK 20", "XXL": "UK 22+"}
        },
        "dress": {
            "female": {"XS": "UK 6", "S": "UK 8–10", "M": "UK 12", "L": "UK 14–16", "XL": "UK 18", "XXL": "UK 20+"}
        }
    }
    return uk_sizes.get(category, {}).get(gender, {}).get(size_label, "Unknown")

def display_size_recommendation(category, gender, age, base_size, user_size):
    sizes = show_size_range(base_size)
    uk_size = convert_to_uk_size(category, user_size, gender)
    item_name = {
        "tshirt": "👕 T-shirt",
        "pants": "👖 Pants",
        "dress": "👗 Dress"
    }.get(category, "Clothing")

    print(f"\nGender: {'Male' if gender == 'male' else 'Female'}")
    print(f"Age: {age}")
    print(f"Clothing type: {item_name.replace('👕 ', '').replace('👖 ', '').replace('👗 ', '')}\n")

    print("📏 Based on your height and weight:")
    print(f"You are most suitable for size {sizes[1]} (Regular fit).")
    print(f"If you want a tighter fit, you may try {sizes[0]}.")
    print(f"If you prefer a looser fit, consider {sizes[2]}.")

    print(f"\n{item_name} size estimated: {user_size} ({uk_size})\n")

def main():
    print("👋 Welcome to the Smart Fit Recommender")

    while True:
        gender_input = input("What is your gender types? (1: Male, 2: Female): ").strip()
        if gender_input == '1':
            gender = "male"
            break
        elif gender_input == '2':
            gender = "female"
            break
        else:
            print("❌ Please enter '1' or '2'.")

    age = get_age_input("Enter your age", 6, 100)
    height = get_user_input("Enter your height in cm", 10, 250, decimals=1)
    weight = get_user_input("Enter your weight in kg", 35, 150, decimals=2)

    base_size = estimate_base_size(height, weight)

    while True:
        print("\nWhich type of clothing are you looking for?")
        print("1) T-shirt")
        print("2) Long pants")
        print("3) Short pants")
        if gender == "female":
            print("4) Dress")
        print("0) Exit")
        choice = input("Enter your choice (0-4): ").strip()

        if choice == '1':
            print("\n🔍 Sizing for T-shirt:")
            sizes = show_size_range(base_size)
            user_size = sizes[1]  # regular fit
            display_size_recommendation("tshirt", gender, age, base_size, user_size)

        elif choice == '2':
            print("\n🔍 Sizing for Long pants:")
            sizes = show_size_range(base_size)
            user_size = sizes[1]
            display_size_recommendation("pants", gender, age, base_size, user_size)

        elif choice == '3':
            print("\n🔍 Sizing for Short pants:")
            print("\nHow long do you prefer your shorts?")
            print("1) Above thigh (closer to muscle area)")
            print("2) Knee-length (more coverage and room)")
            length_choice = input("Enter your choice (1/2): ").strip()

            muscle_adjust = False
            if length_choice == '1':
                muscle_input = input("Do you have muscular or wider thighs? (y/n): ").lower()
                if muscle_input == 'y':
                    muscle_adjust = True

            sizes = show_size_range(base_size)
            user_size = sizes[1]

            if muscle_adjust:
                size_order = ["XS", "S", "M", "L", "XL", "XXL"]
                if user_size in size_order and size_order.index(user_size) < len(size_order) - 1:
                    user_size = size_order[size_order.index(user_size) + 1]

            display_size_recommendation("pants", gender, age, base_size, user_size)

        elif choice == '4' and gender == "female":
            print("\n🔍 Sizing for Dress:")
            sizes = show_size_range(base_size)
            user_size = sizes[1]
            display_size_recommendation("dress", gender, age, base_size, user_size)

        elif choice == '0':
            print("👋 Thank you for using the Smart Fit Recommender. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

        while True:
            cont = input("Would you like to check another clothing item? (1: Yes, 0: No): ").strip()
            if cont in ['1', '0']:
                break
            else:
                print("❌ Invalid input. Please enter 1 or 0.")

        if cont != '1':
            print("👋 Thank you for using the Smart Fit Recommender. Goodbye!")
            break

# Run the program
main()

# Smart Fit Recommender
# This program is a clothing size recommender that helps users find their ideal size based on height and weight.
# This code is a simple clothing size recommender based on user input for height and weight.
# It estimates a base size and provides options for different fits.
# The user can choose between T-shirts and pants, and the program will convert the size to UK sizes.
# The program is designed to be user-friendly with clear prompts and error handling.
# The code is structured to be modular, with functions for each part of the process.
# The main function orchestrates the flow of the program, ensuring a smooth user experience.
# The program is designed to be easily extendable for future clothing categories or size systems.
# The code is written in Python and is intended to be run in a console or terminal.
# The program uses a simple command-line interface for user interaction.
# The code is designed to be clear and easy to understand, with comments explaining each part.
# The program is intended for educational purposes and can be used as a starting point for more complex applications.