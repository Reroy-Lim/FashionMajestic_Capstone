def get_user_input(prompt, min_val, max_val, decimals=0):
    while True:
        try:
            value = float(input(f"{prompt} ({min_val}-{max_val}): "))
            if min_val <= value <= max_val:
                return round(value, decimals)
            else:
                print(f"❌ Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


def get_age_input(prompt, min_val, max_val):
    while True:
        try:
            age = int(input(f"{prompt} ({min_val}-{max_val}): "))
            if min_val <= age <= max_val:
                return age
            else:
                print(f"❌ Please enter an age between {min_val} and {max_val}.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid age.")


def estimate_base_size(height, weight):
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        return "XS"
    elif 18.5 <= bmi < 22:
        return "S"
    elif 22 <= bmi < 25:
        return "M"
    elif 25 <= bmi < 30:
        return "L"
    elif 30 <= bmi < 35:
        return "XL"
    else:
        return "XXL"


def show_size_range(base_size):
    size_order = ["XS", "S", "M", "L", "XL", "XXL"]
    index = size_order.index(base_size)
    lower = size_order[max(0, index - 1)]
    upper = size_order[min(len(size_order) - 1, index + 1)]
    print(f"Recommended size range: {lower} - {upper}")
    return lower, base_size, upper


def display_size_recommendation(clothing_type, gender, age, base_size, user_size):
    print("\n📏 Final Recommendation:")
    print(f"Clothing type: {clothing_type.capitalize()}")
    if gender:
        print(f"Gender: {gender.capitalize()}")
    if age is not None:
        print(f"Age: {age}")
    print(f"Based on your inputs, we recommend size: {user_size}\n")


def main():
    print("👋 Welcome to the Smart Fit Recommender")

    while True:
        print("\nWhich type of clothing are you looking for?")
        print("1) T-shirt")
        print("2) Long pants")
        print("3) Short pants")
        print("4) Dress")
        print("0) Exit")
        
        # Added a loop to validate choice input
        while True:
            choice = input("Enter your choice (0-4): ").strip()
            if choice in ['0', '1', '2', '3', '4']:
                break
            else:
                print("❌ Invalid choice. Please enter a number between 0 and 4.")
        
        if choice == '0':
            print("👋 Thank you for using the Smart Fit Recommender. Goodbye!")
            break

        height = get_user_input("Enter your height in cm", 10, 250, decimals=1)
        weight = get_user_input("Enter your weight in kg", 35, 150, decimals=2)
        base_size = estimate_base_size(height, weight)

        if choice == '1':  # T-shirt
            gender_input = input("What is your gender? (1: Male, 2: Female): ").strip()
            gender = "male" if gender_input == '1' else "female"
            sizes = show_size_range(base_size)
            user_size = sizes[1]
            display_size_recommendation("tshirt", gender, None, base_size, user_size)

        elif choice in ['2', '3']:  # Long or short pants
            gender_input = input("What is your gender? (1: Male, 2: Female): ").strip()
            gender = "male" if gender_input == '1' else "female"
            age = get_age_input("Enter your age", 6, 100)

            if choice == '3':
                print("\nHow long do you prefer your shorts?")
                print("1) Above thigh (closer to muscle area)")
                print("2) Knee-length (more coverage and room)")
                length_choice = input("Enter your choice (1/2): ").strip()

                muscle_adjust = False
                if length_choice == '1':
                    muscle_value = get_user_input(
                        "On a scale of 1 (slim) to 5 (very muscular), how would you rate your thighs?",
                        1, 5, decimals=0
                    )
                    muscle_adjust = muscle_value >= 4

                sizes = show_size_range(base_size)
                user_size = sizes[1]
                if muscle_adjust:
                    size_order = ["XS", "S", "M", "L", "XL", "XXL"]
                    if user_size in size_order and size_order.index(user_size) < len(size_order) - 1:
                        user_size = size_order[size_order.index(user_size) + 1]
                display_size_recommendation("pants", gender, age, base_size, user_size)

            else:
                sizes = show_size_range(base_size)
                user_size = sizes[1]
                display_size_recommendation("pants", gender, age, base_size, user_size)

        elif choice == '4':  # Dress
            age = get_age_input("Enter your age", 6, 100)
            sizes = show_size_range(base_size)
            user_size = sizes[1]
            display_size_recommendation("dress", "female", age, base_size, user_size)

        else:
            print("❌ Invalid choice. Please try again.")
            continue

        # Asking if user wants to check another item
        while True:
            cont = input("Would you like to check another clothing item? (1: Yes, 0: No): ").strip()
            if cont in ['1', '0']:
                break
            else:
                print("❌ Invalid input. Please enter 1 or 0.")
        if cont != '1':
            print("👋 Thank you for using the Smart Fit Recommender. Goodbye!")
            break


if __name__ == "__main__":
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
