"""
UK Size Fit Recommender System
=============================

This program helps users determine their optimal clothing size for UK market based on body measurements.
It takes various inputs (height, weight, optional measurements) and provides size recommendations.

Features:
- Input validation for all measurements
- Gender-specific sizing
- Clothing-type specific adjustments
- Optional detailed measurements for improved accuracy
- Conversion from international sizes to UK sizes
- Size range recommendations (suggesting adjacent sizes that might fit)

Data Flow:
1. User selects clothing type (T-shirt, pants, shorts, dress)
2. System collects basic measurements (height, weight)
3. System optionally collects detailed measurements (chest, waist)
4. System calculates base size using BMI and measurements
5. System applies clothing-type specific adjustments
6. System converts to UK sizing standards
7. System displays recommendation with size range
"""

def get_user_input(prompt: str, min_val: float, max_val: float, decimals: int = 0) -> float:
    """
    Gets and validates numerical user input within specified range and decimal precision.
    
    Args:
        prompt (str): The message displayed to user when asking for input
        min_val (float): Minimum acceptable value
        max_val (float): Maximum acceptable value
        decimals (int): Number of decimal places allowed (0 for integers)
        
    Returns:
        float: Validated numerical value within specified range
        
    Example:
        >>> height = get_user_input("Enter height in cm", 100, 250, 1)
        Enter height in cm: 175.5
        >>> height
        175.5
        
    Validation Process:
    1. Checks if input is numerical (allows only numbers and single decimal point)
    2. Validates decimal places don't exceed specified limit
    3. Verifies value is within min/max range
    4. Repeats prompt until valid input is received
    """
    while True:
        try:
            value = input(f"{prompt}: ")
            
            # Strict numerical validation - allows only numbers and optional single decimal point
            if not value.replace('.', '', 1).isdigit() or value.count('.') > 1:
                print("❌ Only numerical values allowed (no letters/symbols).")
                continue
                
            # Decimal place validation
            if '.' in value:
                integer_part, decimal_part = value.split('.')
                if len(decimal_part) > decimals:
                    print(f"❌ Please enter a value with up to {decimals} decimal places.")
                    continue
            
            value = float(value)
            if min_val <= value <= max_val:
                return round(value, decimals)
            else:
                print(f"❌ Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


def get_age_input(prompt: str, min_val: int, max_val: int) -> int:
    """
    Gets and validates age input from user within specified range.
    
    Args:
        prompt (str): Message displayed to user
        min_val (int): Minimum acceptable age (inclusive)
        max_val (int): Maximum acceptable age (inclusive)
        
    Returns:
        int: Validated age within specified range
        
    Example:
        >>> age = get_age_input("Enter your age", 6, 100)
        Enter your age: 25
        >>> age
        25
        
    Validation Process:
    1. Checks input is a whole number (no decimals)
    2. Verifies age is within specified range
    3. Repeats prompt until valid input is received
    """
    while True:
        try:
            age = input(f"{prompt}: ")
            if not age.isdigit():
                print("❌ Please enter a whole number.")
                continue
                
            age = int(age)
            if min_val <= age <= max_val:
                return age
            else:
                print(f"❌ Please enter an age between {min_val} and {max_val}.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid age.")


def get_gender_input(clothing_type: str) -> str:
    """
    Gets user's gender with validation, with special handling for dresses (female only).
    
    Args:
        clothing_type (str): Type of clothing being selected (tshirt/pants/short pants/dress)
        
    Returns:
        str: "male" or "female"
        
    Example:
        >>> gender = get_gender_input("tshirt")
        Gender (required for accurate sizing):
        1) Male
        2) Female
        Enter your choice (1-2): 1
        >>> gender
        'male'
        
    Special Case:
    - For 'dress' clothing type, automatically returns 'female' without prompting
    """
    if clothing_type == "dress":
        return "female"  # Dresses are typically only for females
    
    while True:
        print("\nGender (required for accurate sizing):")
        print("1) Male")
        print("2) Female")
        choice = input("Enter your choice (1-2): ").strip()
        if choice == '1':
            return "male"
        elif choice == '2':
            return "female"
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")


def get_consent(measurement_type: str) -> bool:
    """
    Gets user consent to use specific measurements for sizing.
    
    Args:
        measurement_type (str): Type of measurement being requested (e.g., "height and weight")
        
    Returns:
        bool: True if consent given (user entered 1), False otherwise (user entered 0)
        
    Example:
        >>> if get_consent("height and weight"):
        ...     # Proceed with measurements
        May we use your height and weight for sizing? (1:Yes, 0:No): 1
        True
    """
    while True:
        consent = input(f"May we use your {measurement_type} for sizing? (1:Yes, 0:No): ").strip()
        if consent == '1':
            return True
        elif consent == '0':
            return False
        else:
            print("❌ Invalid input. Please enter 1 or 0.")


def get_optional_measurement(measurement_type: str, clothing_type: str) -> float | None:
    """
    Gets optional body measurements with range selection and consent.
    
    Args:
        measurement_type (str): "chest" or "waist" measurement
        clothing_type (str): Type of clothing being selected (affects measurement ranges)
        
    Returns:
        float | None: Midpoint of selected range if provided, None if skipped
        
    Example:
        >>> chest_size = get_optional_measurement('chest', 'tshirt')
        Optional chest measurement (for improved accuracy):
        0) Skip - use height/weight only
        1) 60-91cm (XS-S sizes)
        2) 92-122cm (M-L sizes)
        3) 123-153cm (XL sizes)
        4) 154-184cm (XXL sizes)
        Select chest range (0-4): 2
        May we use your chest for sizing? (1:Yes, 0:No): 1
        >>> chest_size
        107.0  # Midpoint of 92-122cm range
        
    Measurement Ranges:
    - For dresses:
      * Chest: 
        1) 80-90cm (Small frame)
        2) 91-100cm (Medium frame)
        3) 101-110cm (Large frame)
        4) 111-120cm (Extra large frame)
      * Waist:
        1) 60-70cm (Small waist)
        2) 71-80cm (Medium waist)
        3) 81-90cm (Large waist)
        4) 91-100cm (Extra large waist)
        
    - For other clothing types:
      * Chest/Waist:
        1) 60-91cm (XS-S sizes)
        2) 92-122cm (M-L sizes)
        3) 123-153cm (XL sizes)
        4) 154-184cm (XXL sizes)
    """
    # Different measurement ranges based on clothing type
    if clothing_type == "dress":
        ranges = {
            'chest': [
                ("80-90cm (Small frame)", 80, 90),     # Range 1: Small frame
                ("91-100cm (Medium frame)", 91, 100),  # Range 2: Medium frame
                ("101-110cm (Large frame)", 101, 110), # Range 3: Large frame
                ("111-120cm (Extra large frame)", 111, 120)  # Range 4: Extra large frame
            ],
            'waist': [
                ("60-70cm (Small waist)", 60, 70),     # Range 1: Small waist
                ("71-80cm (Medium waist)", 71, 80),    # Range 2: Medium waist
                ("81-90cm (Large waist)", 81, 90),     # Range 3: Large waist
                ("91-100cm (Extra large waist)", 91, 100)    # Range 4: Extra large waist
            ]
        }
    else:
        ranges = {
            'chest': [
                ("60-91cm (XS-S sizes)", 60, 91),      # Range 1: XS-S sizes
                ("92-122cm (M-L sizes)", 92, 122),     # Range 2: M-L sizes
                ("123-153cm (XL sizes)", 123, 153),   # Range 3: XL sizes
                ("154-184cm (XXL sizes)", 154, 184)    # Range 4: XXL sizes
            ],
            'waist': [
                ("60-91cm (XS-S sizes)", 60, 91),     # Range 1: XS-S sizes
                ("92-122cm (M-L sizes)", 92, 122),    # Range 2: M-L sizes
                ("123-153cm (XL sizes)", 123, 153),   # Range 3: XL sizes
                ("154-184cm (XXL sizes)", 154, 184)   # Range 4: XXL sizes
            ]
        }
    
    print(f"\nOptional {measurement_type} measurement (for improved accuracy):")
    print("0) Skip - use height/weight only")
    for i, (label, _, _) in enumerate(ranges[measurement_type], 1):
        print(f"{i}) {label}")
    
    while True:
        choice = input(f"Select {measurement_type} range (0-{len(ranges[measurement_type])}): ").strip()
        if choice == '0':
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(ranges[measurement_type]):
            if not get_consent(measurement_type):
                print(f"❌ {measurement_type.capitalize()} measurement not used.")
                return None
            selected_range = ranges[measurement_type][int(choice)-1]
            return (selected_range[1] + selected_range[2]) / 2  # Return midpoint
        print(f"❌ Please enter 0-{len(ranges[measurement_type])}")


def estimate_base_size(height: float, weight: float, chest: float | None = None, 
                      waist: float | None = None, clothing_type: str | None = None) -> str:
    """
    Estimates base clothing size using BMI and optional measurements.
    
    Args:
        height (float): Height in cm (100-250)
        weight (float): Weight in kg (30-200)
        chest (float | None): Optional chest measurement in cm
        waist (float | None): Optional waist measurement in cm
        clothing_type (str | None): Type of clothing being sized
        
    Returns:
        str: Estimated size (XS, S, M, L, XL, XXL)
        
    Example:
        >>> estimate_base_size(175, 70, 95, 80, 'tshirt')
        'M'
        
    Size Calculation Logic:
    1. Calculate BMI = weight(kg) / (height(m)^2)
    2. Initial size based on BMI ranges:
       - BMI < 18.5: XS
       - 18.5 ≤ BMI < 22: S
       - 22 ≤ BMI < 25: M
       - 25 ≤ BMI < 30: L
       - 30 ≤ BMI < 35: XL
       - BMI ≥ 35: XXL
    3. Adjust size upward if:
       - Chest measurement exceeds threshold (100 for dresses, 122 otherwise)
       - Waist measurement exceeds threshold (80 for dresses, 122 otherwise)
    """
    bmi = weight / ((height / 100) ** 2)
    
    # Initial size based on BMI
    if bmi < 18.5:
        size = "XS"
    elif 18.5 <= bmi < 22:
        size = "S"
    elif 22 <= bmi < 25:
        size = "M"
    elif 25 <= bmi < 30:
        size = "L"
    elif 30 <= bmi < 35:
        size = "XL"
    else:
        size = "XXL"
    
    # Adjust based on measurements if provided
    size_order = ["XS", "S", "M", "L", "XL", "XXL"]
    
    if chest:
        if clothing_type == "dress":
            threshold = 100 if size in ["XS", "S"] else 110
        else:
            threshold = 122
        
        if chest > threshold and size_order.index(size) < len(size_order) - 1:
            size = size_order[size_order.index(size) + 1]
    
    if waist:
        if clothing_type == "dress":
            threshold = 80 if size in ["XS", "S"] else 90
        else:
            threshold = 122
        
        if waist > threshold and size_order.index(size) < len(size_order) - 1:
            size = size_order[size_order.index(size) + 1]
    
    return size


def convert_to_uk(size: str, clothing_type: str, gender: str) -> str:
    """
    Converts international size to UK size based on clothing type and gender.
    
    Args:
        size (str): International size (XS, S, M, L, XL, XXL)
        clothing_type (str): Type of clothing (tshirt/pants/short pants/dress)
        gender (str): "male" or "female"
        
    Returns:
        str: UK size designation
        
    Example:
        >>> convert_to_uk("M", "tshirt", "male")
        'UK 38'
        
    Conversion Tables:
    - Male T-shirts:
      XS: UK 34, S: UK 36, M: UK 38, L: UK 40, XL: UK 42, XXL: UK 44
    - Female T-shirts:
      XS: UK 6, S: UK 8, M: UK 10, L: UK 12, XL: UK 14, XXL: UK 16
    - Male Pants:
      XS: UK 30, S: UK 32, M: UK 34, L: UK 36, XL: UK 38, XXL: UK 40
    - Female Pants:
      XS: UK 8, S: UK 10, M: UK 12, L: UK 14, XL: UK 16, XXL: UK 18
    - Dresses:
      XS: UK 8, S: UK 10, M: UK 12, L: UK 14, XL: UK 16, XXL: UK 18
    """
    # UK size conversion tables
    male_tshirt = {"XS": "UK 34", "S": "UK 36", "M": "UK 38", 
                  "L": "UK 40", "XL": "UK 42", "XXL": "UK 44"}
    
    female_tshirt = {"XS": "UK 6", "S": "UK 8", "M": "UK 10",
                    "L": "UK 12", "XL": "UK 14", "XXL": "UK 16"}
    
    male_pants = {"XS": "UK 30", "S": "UK 32", "M": "UK 34",
                 "L": "UK 36", "XL": "UK 38", "XXL": "UK 40"}
    
    female_pants = {"XS": "UK 8", "S": "UK 10", "M": "UK 12",
                   "L": "UK 14", "XL": "UK 16", "XXL": "UK 18"}
    
    dress_sizes = {"XS": "UK 8", "S": "UK 10", "M": "UK 12",
                  "L": "UK 14", "XL": "UK 16", "XXL": "UK 18"}
    
    if clothing_type == "tshirt":
        return male_tshirt[size] if gender == "male" else female_tshirt[size]
    elif clothing_type in ["pants", "short pants"]:
        return male_pants[size] if gender == "male" else female_pants[size]
    else:  # dress
        return dress_sizes[size]


def show_size_range(base_size: str, clothing_type: str, gender: str) -> tuple[str, str, str]:
    """
    Displays recommended size range and adjacent possible sizes.
    
    Args:
        base_size (str): Primary recommended size (XS-XXL)
        clothing_type (str): Type of clothing
        gender (str): "male" or "female"
        
    Returns:
        tuple: (lower_size, base_size, upper_size) - adjacent sizes in the size spectrum
        
    Example:
        >>> show_size_range("M", "pants", "male")
        Recommended size range: M (UK 34)
        May also fit: S-XL (UK 32-38)
        ('S', 'M', 'L')
    """
    size_order = ["XS", "S", "M", "L", "XL", "XXL"]
    index = size_order.index(base_size)
    lower = size_order[max(0, index - 1)]
    upper = size_order[min(len(size_order) - 1, index + 1)]
    
    print(f"\nRecommended size range: {base_size} (UK {convert_to_uk(base_size, clothing_type, gender)})")
    print(f"May also fit: {lower}-{upper} (UK {convert_to_uk(lower, clothing_type, gender)}-{convert_to_uk(upper, clothing_type, gender)})")
    
    return lower, base_size, upper


def display_size_recommendation(clothing_type: str, gender: str | None, age: int | None, 
                               base_size: str, uk_size: str) -> None:
    """
    Displays final size recommendation with all relevant details.
    
    Args:
        clothing_type (str): Type of clothing
        gender (str | None): User's gender if relevant
        age (int | None): User's age if relevant
        base_size (str): International size (XS-XXL)
        uk_size (str): UK size equivalent
        
    Example:
        >>> display_size_recommendation("tshirt", "male", 30, "M", "UK 38")
        📏 Final Recommendation:
        Clothing type: T-shirt
        Gender: Male
        Age: 30
        International size: M
        UK size: UK 38
    """
    print("\n📏 Final Recommendation:")
    print(f"Clothing type: {clothing_type.capitalize()}")
    if gender:  # Only show gender if it's relevant
        print(f"Gender: {gender.capitalize()}")
    if age is not None:
        print(f"Age: {age}")
    print(f"International size: {base_size}")
    print(f"UK size: {uk_size}\n")


def main() -> None:
    """
    Main function that runs the UK Size Fit Recommender program.
    Coordinates the entire sizing process from user input to final recommendation.
    
    Program Flow:
    1. Display welcome message
    2. Get clothing type selection
    3. Collect basic measurements (height, weight)
    4. Get gender input (except for dresses)
    5. Collect optional measurements (chest, waist)
    6. Calculate base size using BMI and measurements
    7. Apply clothing-specific adjustments:
       - Short pants: Consider thigh muscle rating
       - Pants/Dress: Consider age
    8. Convert to UK sizing
    9. Display recommendation with size range
    10. Offer to check another item or exit
    
    Example Usage:
    >>> main()
    👋 Welcome to the UK Size Fit Recommender
    Note: We only use your data for sizing and don't store it.
    ...
    """
    print("👋 Welcome to the UK Size Fit Recommender")
    print("Note: We only use your data for sizing and don't store it.\n")

    while True:
        print("\nWhich type of clothing are you looking for?")
        print("1) T-shirt")
        print("2) Long pants")
        print("3) Short pants")
        print("4) Dress")
        print("0) Exit")
        
        choice = input("Enter your choice (0-4): ").strip()
        if choice == '0':
            print("👋 Thank you for using the UK Size Fit Recommender. Goodbye!")
            break
        if choice not in ['1', '2', '3', '4']:
            print("❌ Invalid choice. Please try again.")
            continue

        # Map choice to clothing type
        clothing_type = {
            '1': 'tshirt',
            '2': 'pants',
            '3': 'short pants',
            '4': 'dress'
        }[choice]

        # Get consent for basic measurements
        print("\nWe need your basic measurements for sizing:")
        if not get_consent("height and weight"):
            print("⚠️ Cannot provide recommendations without basic measurements.")
            continue
            
        # Get required inputs
        height = get_user_input("Height in cm (e.g. 172 or 172.5)", 100, 250, 1)
        weight = get_user_input("Weight in kg (e.g. 68 or 68.50)", 30, 200, 2)
        gender = get_gender_input(clothing_type)
        
        # Get optional measurements
        chest = get_optional_measurement('chest', clothing_type)
        waist = get_optional_measurement('waist', clothing_type)
        
        # Calculate final size with clothing type context
        base_size = estimate_base_size(height, weight, chest, waist, clothing_type)

        # Special adjustments based on clothing type
        if choice == '3':  # Short pants
            age = get_age_input("Enter your age", 6, 100)
            
            print("\nHow long do you prefer your shorts?")
            print("1) Above thigh (closer to muscle area)")
            print("2) Knee-length (more coverage and room)")
            length_choice = input("Enter your choice (1-2): ").strip()

            if length_choice == '1':
                muscle_value = get_user_input(
                    "On a scale of 1 (slim) to 5 (very muscular), how would you rate your thighs?",
                    1, 5, 0
                )
                if muscle_value >= 4:
                    size_order = ["XS", "S", "M", "L", "XL", "XXL"]
                    if base_size in size_order and size_order.index(base_size) < len(size_order) - 1:
                        base_size = size_order[size_order.index(base_size) + 1]
        elif choice in ['2', '4']:  # Pants or dress
            age = get_age_input("Enter your age", 6, 100)

        # Show results
        sizes = show_size_range(base_size, clothing_type, gender)
        uk_size = convert_to_uk(base_size, clothing_type, gender)
        display_size_recommendation(
            clothing_type, 
            gender if clothing_type != "dress" else None,  # Hide gender for dresses
            age if choice != '1' else None, 
            base_size, 
            uk_size
        )

        # Continue prompt
        while True:
            cont = input("Would you like to check another clothing item? (1:Yes, 0:No): ").strip()
            if cont in ['1', '0']:
                break
            print("❌ Invalid input. Please enter 1 or 0.")
        if cont != '1':
            print("👋 Thank you for using the UK Size Fit Recommender. Goodbye!")
            break


if __name__ == "__main__":
    main()
