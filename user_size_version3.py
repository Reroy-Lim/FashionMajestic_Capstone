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

# Lecturer's Comments:
# - Good use of docstrings for module-level documentation
# - Consider adding version number and author information
# - Example: __version__ = '1.0.0', __author__ = 'Your Name'
"""

import os  # Import for file path operations
import sys  # Import for system-specific parameters
import json  # Import for JSON operations
import logging  # Import for logging operations
import logging.handlers  # Import for logging handlers
import datetime  # Import for timestamp operations
import enum  # Import for enumeration support
import dataclasses  # Import for data class support

# Constants for the application
CLOTHING_TYPES = enum.Enum('ClothingType', ['TSHIRT', 'PANTS', 'SHORT_PANTS', 'DRESS'])  # Define clothing types as enum for type safety
SIZE_ORDER = ["XS", "S", "M", "L", "XL", "XXL"]  # Define size order as constant
MIN_AGE = 6  # Define minimum age as constant
MAX_AGE = 100  # Define maximum age as constant

# Configure logging
def setup_logging(logfile: str) -> None:
    """
    Sets up logging configuration for the application.
    Creates a rotating file handler that creates new log file each day.
    
    Example:
        >>> setup_logging()
        >>> logging.info("Application started")  # Writes to log file
    """
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')  # Create logs directory in same folder as script
    os.makedirs(log_dir, exist_ok=True)  # Create logs directory if it doesn't exist
    
    log_file = os.path.join(log_dir, logfile)  # Define log file path
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )  # Define log format
    
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when='midnight',
        interval=1,
        backupCount=30
    )  # Create rotating file handler
    file_handler.setFormatter(formatter)  # Set formatter for file handler
    
    console_handler = logging.StreamHandler(sys.stdout)  # Create console handler
    console_handler.setFormatter(formatter)  # Set formatter for console handler
    
    logger = logging.getLogger()  # Get root logger
    logger.setLevel(logging.INFO)  # Set logging level
    logger.addHandler(file_handler)  # Add file handler to logger
    logger.addHandler(console_handler)  # Add console handler to logger

# Initialize logging when module is imported
setup_logging(logfile = "size_recommender.log")  # Set up logging configuration

# Data class for user measurements
@dataclasses.dataclass
class UserMeasurements:
    """
    Data class to store user measurements.
    Provides type hints and validation for measurements.
    
    Example:
        >>> measurements = UserMeasurements(height=175.0, weight=70.0)
        >>> print(measurements.height)
        175.0
    """
    height: float  # Height in centimeters
    weight: float  # Weight in kilograms
    chest: float | None = None  # Optional chest measurement in centimeters
    waist: float | None = None  # Optional waist measurement in centimeters
    age: int | None = None  # Optional age in years
    
    def __post_init__(self) -> None:
        """Validates measurements after initialization."""
        if not 100 <= self.height <= 250:  # Validate height range
            raise ValueError(f"Height must be between 100 and 250 cm, got {self.height}")
        if not 30 <= self.weight <= 200:  # Validate weight range
            raise ValueError(f"Weight must be between 30 and 200 kg, got {self.weight}")
        if self.age is not None and not MIN_AGE <= self.age <= MAX_AGE:  # Validate age range if provided
            raise ValueError(f"Age must be between {MIN_AGE} and {MAX_AGE} years, got {self.age}")

def validate_numeric_input(value: str, min_val: float, max_val: float, decimals: int = 0) -> float:
    """
    Validates numeric input string against specified constraints.
    
    Args:
        value (str): Input string to validate
        min_val (float): Minimum acceptable value
        max_val (float): Maximum acceptable value
        decimals (int): Number of decimal places allowed
        
    Returns:
        float: Validated numerical value
        
    Raises:
        ValueError: If input is invalid
        
    Example:
        >>> validate_numeric_input("175.5", 100, 250, 1)
        175.5
    """
    if not value.replace('.', '', 1).isdigit() or value.count('.') > 1:  # Check if input is numeric with at most one decimal point
        raise ValueError("Input must be numeric with at most one decimal point")
        
    if '.' in value:  # Check decimal places if input has decimal point
        integer_part, decimal_part = value.split('.')
        if len(decimal_part) > decimals:
            raise ValueError(f"Input must have at most {decimals} decimal places")
    
    num_value = float(value)  # Convert to float
    if not min_val <= num_value <= max_val:  # Check value range
        raise ValueError(f"Input must be between {min_val} and {max_val}")
        
    return round(num_value, decimals)  # Round to specified decimal places

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
    """
    while True:  # Loop until valid input is received
        try:
            value = input(f"{prompt}: ").strip()  # Get input and remove whitespace
            logging.debug(f"Received input: {value} for prompt: {prompt}")  # Log received input
            
            result = validate_numeric_input(value, min_val, max_val, decimals)  # Validate input
            logging.info(f"Valid input received: {result} for {prompt}")  # Log valid input
            return result
            
        except ValueError as e:  # Handle validation errors
            error_msg = f"❌ {str(e)}"  # Create error message
            print(error_msg)  # Display error to user
            logging.warning(f"Invalid input: {value} - {str(e)}")  # Log error

def get_age_input(prompt: str, min_val: int = MIN_AGE, max_val: int = MAX_AGE) -> int:
    """
    Gets and validates age input from user within specified range.
    
    Args:
        prompt (str): Message displayed to user
        min_val (int): Minimum acceptable age (inclusive)
        max_val (int): Maximum acceptable age (inclusive)
        
    Returns:
        int: Validated age within specified range
        
    Example:
        >>> age = get_age_input("Enter your age")
        Enter your age: 25
        >>> age
        25
    """
    while True:  # Loop until valid input is received
        try:
            age = input(f"{prompt}: ").strip()  # Get input and remove whitespace
            logging.debug(f"Received age input: {age}")  # Log received input
            
            if not age.isdigit():  # Check if input is a whole number
                raise ValueError("Age must be a whole number")
                
            age_value = int(age)  # Convert to integer
            if not min_val <= age_value <= max_val:  # Check age range
                raise ValueError(f"Age must be between {min_val} and {max_val}")
                
            logging.info(f"Valid age input received: {age_value}")  # Log valid input
            return age_value
            
        except ValueError as e:  # Handle validation errors
            error_msg = f"❌ {str(e)}"  # Create error message
            print(error_msg)  # Display error to user
            logging.warning(f"Invalid age input: {age} - {str(e)}")  # Log error

def get_gender_input(clothing_type: str) -> str:
    """
    Gets user's gender with validation, with special handling for dresses (female only).
    
    Args:
        clothing_type (str): Type of clothing being selected
        
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
    """
    if clothing_type == CLOTHING_TYPES.DRESS.name.lower():  # Check if clothing type is dress
        logging.info("Dress selected, automatically setting gender to female")  # Log automatic gender selection
        return "female"  # Return female for dresses
    
    while True:  # Loop until valid input is received
        try:
            print("\nGender (required for accurate sizing):")  # Display prompt
            print("1) Male")  # Display male option
            print("2) Female")  # Display female option
            
            choice = input("Enter your choice (1-2): ").strip()  # Get input and remove whitespace
            logging.debug(f"Received gender choice: {choice}")  # Log received input
            
            if choice not in ['1', '2']:  # Validate input
                raise ValueError("Please enter 1 or 2")
                
            gender = "male" if choice == '1' else "female"  # Convert choice to gender
            logging.info(f"Valid gender selected: {gender}")  # Log valid selection
            return gender
            
        except ValueError as e:  # Handle validation errors
            error_msg = f"❌ {str(e)}"  # Create error message
            print(error_msg)  # Display error to user
            logging.warning(f"Invalid gender choice: {choice} - {str(e)}")  # Log error

def get_consent(measurement_type: str) -> bool:
    """
    Gets user consent to use specific measurements for sizing.
    
    Args:
        measurement_type (str): Type of measurement being requested
        
    Returns:
        bool: True if consent given, False otherwise
        
    Example:
        >>> if get_consent("height and weight"):
        ...     # Proceed with measurements
        May we use your height and weight for sizing? (1:Yes, 0:No): 1
        True
    """
    while True:  # Loop until valid input is received
        try:
            consent = input(f"May we use your {measurement_type} for sizing? (1:Yes, 0:No): ").strip()  # Get input and remove whitespace
            logging.debug(f"Received consent input: {consent} for {measurement_type}")  # Log received input
            
            if consent not in ['0', '1']:  # Validate input
                raise ValueError("Please enter 1 for Yes or 0 for No")
                
            result = consent == '1'  # Convert input to boolean
            logging.info(f"Consent {'given' if result else 'denied'} for {measurement_type}")  # Log consent decision
            return result
            
        except ValueError as e:  # Handle validation errors
            error_msg = f"❌ {str(e)}"  # Create error message
            print(error_msg)  # Display error to user
            logging.warning(f"Invalid consent input: {consent} - {str(e)}")  # Log error

def get_optional_measurement(measurement_type: str, clothing_type: str) -> float | None:
    """
    Gets optional body measurements with range selection and consent.
    
    Args:
        measurement_type (str): "chest" or "waist" measurement
        clothing_type (str): Type of clothing being selected
        
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
        >>> chest_size
        107.0
    """
    # Define measurement ranges based on clothing type
    ranges = {
        CLOTHING_TYPES.DRESS.name.lower(): {  # Ranges for dresses
            'chest': [
                ("80-90cm (Small frame)", 80, 90),
                ("91-100cm (Medium frame)", 91, 100),
                ("101-110cm (Large frame)", 101, 110),
                ("111-120cm (Extra large frame)", 111, 120)
            ],
            'waist': [
                ("60-70cm (Small waist)", 60, 70),
                ("71-80cm (Medium waist)", 71, 80),
                ("81-90cm (Large waist)", 81, 90),
                ("91-100cm (Extra large waist)", 91, 100)
            ]
        },
        'default': {  # Default ranges for other clothing types
            'chest': [
                ("60-91cm (XS-S sizes)", 60, 91),
                ("92-122cm (M-L sizes)", 92, 122),
                ("123-153cm (XL sizes)", 123, 153),
                ("154-184cm (XXL sizes)", 154, 184)
            ],
            'waist': [
                ("60-91cm (XS-S sizes)", 60, 91),
                ("92-122cm (M-L sizes)", 92, 122),
                ("123-153cm (XL sizes)", 123, 153),
                ("154-184cm (XXL sizes)", 154, 184)
            ]
        }
    }
    
    # Get appropriate ranges for clothing type
    selected_ranges = ranges[clothing_type if clothing_type == CLOTHING_TYPES.DRESS.name.lower() else 'default']
    measurement_ranges = selected_ranges[measurement_type]
    
    logging.debug(f"Using {clothing_type} ranges for {measurement_type} measurement")  # Log range selection
    
    # Display measurement options
    print(f"\nOptional {measurement_type} measurement (for improved accuracy):")
    print("0) Skip - use height/weight only")
    for i, (label, _, _) in enumerate(measurement_ranges, 1):
        print(f"{i}) {label}")
    
    while True:  # Loop until valid input is received
        try:
            choice = input(f"Select {measurement_type} range (0-{len(measurement_ranges)}): ").strip()  # Get input
            logging.debug(f"Received measurement choice: {choice} for {measurement_type}")  # Log received input
            
            if choice == '0':  # Handle skip option
                logging.info(f"{measurement_type.capitalize()} measurement skipped")  # Log skip decision
                return None
                
            if not choice.isdigit() or not 1 <= int(choice) <= len(measurement_ranges):  # Validate input
                raise ValueError(f"Please enter 0-{len(measurement_ranges)}")
                
            if not get_consent(measurement_type):  # Get consent for measurement
                logging.info(f"{measurement_type.capitalize()} measurement not used (consent denied)")  # Log consent denial
                return None
                
            selected_range = measurement_ranges[int(choice)-1]  # Get selected range
            result = (selected_range[1] + selected_range[2]) / 2  # Calculate midpoint
            
            logging.info(f"Valid {measurement_type} measurement selected: {result}cm")  # Log valid selection
            return result
            
        except ValueError as e:  # Handle validation errors
            error_msg = f"❌ {str(e)}"  # Create error message
            print(error_msg)  # Display error to user
            logging.warning(f"Invalid measurement choice: {choice} - {str(e)}")  # Log error

def calculate_bmi(height: float, weight: float) -> float:
    """
    Calculates Body Mass Index (BMI) from height and weight.
    
    Args:
        height (float): Height in centimeters
        weight (float): Weight in kilograms
        
    Returns:
        float: Calculated BMI value
        
    Example:
        >>> calculate_bmi(175, 70)
        22.86
    """
    try:
        height_m = height / 100  # Convert height to meters
        bmi = weight / (height_m ** 2)  # Calculate BMI
        logging.debug(f"Calculated BMI: {bmi:.2f} from height: {height}cm and weight: {weight}kg")  # Log calculation
        return bmi
    except ZeroDivisionError:  # Handle division by zero
        logging.error(f"BMI calculation failed: height cannot be zero")  # Log error
        raise ValueError("Height cannot be zero")
    except Exception as e:  # Handle other errors
        logging.error(f"BMI calculation failed: {str(e)}")  # Log error
        raise

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
    """
    try:
        # Create UserMeasurements instance for validation
        measurements = UserMeasurements(height=height, weight=weight, chest=chest, waist=waist)
        
        # Calculate BMI
        bmi = calculate_bmi(height, weight)
        logging.debug(f"Using BMI {bmi:.2f} for initial size estimation")  # Log BMI usage
        
        # Determine initial size based on BMI
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
            
        logging.info(f"Initial size based on BMI: {size}")  # Log initial size
        
        # Adjust size based on measurements if provided
        if chest:
            threshold = 100 if clothing_type == CLOTHING_TYPES.DRESS.name.lower() and size in ["XS", "S"] else 110
            if chest > threshold and SIZE_ORDER.index(size) < len(SIZE_ORDER) - 1:
                size = SIZE_ORDER[SIZE_ORDER.index(size) + 1]
                logging.info(f"Size adjusted to {size} based on chest measurement")  # Log size adjustment
        
        if waist:
            threshold = 80 if clothing_type == CLOTHING_TYPES.DRESS.name.lower() and size in ["XS", "S"] else 90
            if waist > threshold and SIZE_ORDER.index(size) < len(SIZE_ORDER) - 1:
                size = SIZE_ORDER[SIZE_ORDER.index(size) + 1]
                logging.info(f"Size adjusted to {size} based on waist measurement")  # Log size adjustment
        
        return size
        
    except Exception as e:  # Handle any errors
        logging.error(f"Size estimation failed: {str(e)}")  # Log error
        raise

def convert_to_uk(size: str, clothing_type: str, gender: str) -> str:
    """
    Converts international size to UK size based on clothing type and gender.
    
    Args:
        size (str): International size (XS, S, M, L, XL, XXL)
        clothing_type (str): Type of clothing
        gender (str): "male" or "female"
        
    Returns:
        str: UK size designation
        
    Example:
        >>> convert_to_uk("M", "tshirt", "male")
        'UK 38'
    """
    try:
        # Validate inputs
        if size not in SIZE_ORDER:  # Check size is valid
            raise ValueError(f"Invalid size: {size}")
        if clothing_type not in [t.name.lower() for t in CLOTHING_TYPES]:  # Check clothing type is valid
            raise ValueError(f"Invalid clothing type: {clothing_type}")
        if gender not in ["male", "female"]:  # Check gender is valid
            raise ValueError(f"Invalid gender: {gender}")
            
        # Define size conversion tables
        size_tables = {
            "male_tshirt": {"XS": "UK 34", "S": "UK 36", "M": "UK 38", 
                           "L": "UK 40", "XL": "UK 42", "XXL": "UK 44"},
            "female_tshirt": {"XS": "UK 6", "S": "UK 8", "M": "UK 10",
                            "L": "UK 12", "XL": "UK 14", "XXL": "UK 16"},
            "male_pants": {"XS": "UK 30", "S": "UK 32", "M": "UK 34",
                         "L": "UK 36", "XL": "UK 38", "XXL": "UK 40"},
            "female_pants": {"XS": "UK 8", "S": "UK 10", "M": "UK 12",
                           "L": "UK 14", "XL": "UK 16", "XXL": "UK 18"},
            "dress": {"XS": "UK 8", "S": "UK 10", "M": "UK 12",
                     "L": "UK 14", "XL": "UK 16", "XXL": "UK 18"}
        }
        
        # Select appropriate conversion table
        if clothing_type == CLOTHING_TYPES.TSHIRT.name.lower():
            table_key = f"{gender}_tshirt"
        elif clothing_type in [CLOTHING_TYPES.PANTS.name.lower(), CLOTHING_TYPES.SHORT_PANTS.name.lower()]:
            table_key = f"{gender}_pants"
        else:  # dress
            table_key = "dress"
            
        uk_size = size_tables[table_key][size]  # Convert size
        logging.info(f"Converted {size} to {uk_size} for {gender} {clothing_type}")  # Log conversion
        return uk_size
        
    except Exception as e:  # Handle any errors
        logging.error(f"Size conversion failed: {str(e)}")  # Log error
        raise

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
    try:
        # Get adjacent sizes
        index = SIZE_ORDER.index(base_size)  # Get index of base size
        lower = SIZE_ORDER[max(0, index - 1)]  # Get lower size
        upper = SIZE_ORDER[min(len(SIZE_ORDER) - 1, index + 1)]  # Get upper size
        
        # Convert sizes to UK sizes
        base_uk = convert_to_uk(base_size, clothing_type, gender)  # Convert base size
        lower_uk = convert_to_uk(lower, clothing_type, gender)  # Convert lower size
        upper_uk = convert_to_uk(upper, clothing_type, gender)  # Convert upper size
        
        # Display recommendations
        print(f"\nRecommended size range: {base_size} ({base_uk})")  # Show base size
        print(f"May also fit: {lower}-{upper} ({lower_uk}-{upper_uk})")  # Show size range
        
        logging.info(f"Size range displayed: {lower}-{upper} ({lower_uk}-{upper_uk})")  # Log display
        return lower, base_size, upper
        
    except Exception as e:  # Handle any errors
        logging.error(f"Size range display failed: {str(e)}")  # Log error
        raise

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
    try:
        # Format clothing type for display
        display_type = clothing_type.capitalize()  # Capitalize clothing type
        if clothing_type == CLOTHING_TYPES.TSHIRT.name.lower():  # Special case for T-shirt
            display_type = "T-shirt"
            
        # Display recommendations
        print("\n📏 Final Recommendation:")  # Show header
        print(f"Clothing type: {display_type}")  # Show clothing type
        if gender:  # Show gender if relevant
            print(f"Gender: {gender.capitalize()}")
        if age is not None:  # Show age if provided
            print(f"Age: {age}")
        print(f"International size: {base_size}")  # Show international size
        print(f"UK size: {uk_size}\n")  # Show UK size
        
        # Log recommendation
        log_data = {
            "clothing_type": clothing_type,
            "gender": gender,
            "age": age,
            "base_size": base_size,
            "uk_size": uk_size
        }
        logging.info(f"Final recommendation displayed: {json.dumps(log_data)}")  # Log recommendation
        
    except Exception as e:  # Handle any errors
        logging.error(f"Recommendation display failed: {str(e)}")  # Log error
        raise

def main() -> None:
    """
    Main function that runs the UK Size Fit Recommender program.
    Coordinates the entire sizing process from user input to final recommendation.
    
    Example:
        >>> main()
        👋 Welcome to the UK Size Fit Recommender
        Note: We only use your data for sizing and don't store it.
        ...
    """
    try:
        logging.info("Starting UK Size Fit Recommender")  # Log program start
        
        # Display welcome message
        print("👋 Welcome to the UK Size Fit Recommender")  # Show welcome message
        print("Note: We only use your data for sizing and don't store it.\n")  # Show privacy notice
        
        while True:  # Main program loop
            try:
                # Display clothing type menu
                print("\nWhich type of clothing are you looking for?")  # Show menu header
                print("1) T-shirt")  # Show T-shirt option
                print("2) Long pants")  # Show pants option
                print("3) Short pants")  # Show shorts option
                print("4) Dress")  # Show dress option
                print("0) Exit")  # Show exit option
                
                # Get clothing type choice
                choice = input("Enter your choice (0-4): ").strip()  # Get input
                logging.debug(f"Received clothing choice: {choice}")  # Log received input
                
                if choice == '0':  # Handle exit
                    print("👋 Thank you for using the UK Size Fit Recommender. Goodbye!")  # Show goodbye message
                    logging.info("Program terminated by user")  # Log user exit
                    break
                    
                if choice not in ['1', '2', '3', '4']:  # Validate input
                    print("❌ Invalid choice. Please try again.")  # Show error message
                    logging.warning(f"Invalid clothing choice: {choice}")  # Log invalid input
                    continue
                
                # Map choice to clothing type
                clothing_type = {
                    '1': CLOTHING_TYPES.TSHIRT.name.lower(),
                    '2': CLOTHING_TYPES.PANTS.name.lower(),
                    '3': CLOTHING_TYPES.SHORT_PANTS.name.lower(),
                    '4': CLOTHING_TYPES.DRESS.name.lower()
                }[choice]
                logging.info(f"Selected clothing type: {clothing_type}")  # Log clothing type selection
                
                # Get consent for basic measurements
                print("\nWe need your basic measurements for sizing:")  # Show consent prompt
                if not get_consent("height and weight"):  # Get consent
                    print("⚠️ Cannot provide recommendations without basic measurements.")  # Show error message
                    logging.warning("Basic measurements consent denied")  # Log consent denial
                    continue
                
                # Get required inputs
                height = get_user_input("Height in cm (e.g. 172 or 172.5)", 100, 250, 1)  # Get height
                weight = get_user_input("Weight in kg (e.g. 68 or 68.50)", 30, 200, 2)  # Get weight
                gender = get_gender_input(clothing_type)  # Get gender
                
                # Get optional measurements
                chest = get_optional_measurement('chest', clothing_type)  # Get chest measurement
                waist = get_optional_measurement('waist', clothing_type)  # Get waist measurement
                
                # Calculate final size with clothing type context
                base_size = estimate_base_size(height, weight, chest, waist, clothing_type)  # Calculate size
                
                # Special adjustments based on clothing type
                age = None  # Initialize age
                if choice == '3':  # Handle short pants
                    age = get_age_input("Enter your age")  # Get age
                    
                    print("\nHow long do you prefer your shorts?")  # Show length preference prompt
                    print("1) Above thigh (closer to muscle area)")  # Show above thigh option
                    print("2) Knee-length (more coverage and room)")  # Show knee-length option
                    length_choice = input("Enter your choice (1-2): ").strip()  # Get length preference
                    
                    if length_choice == '1':  # Handle above thigh preference
                        muscle_value = get_user_input(
                            "On a scale of 1 (slim) to 5 (very muscular), how would you rate your thighs?",
                            1, 5, 0
                        )  # Get muscle rating
                        if muscle_value >= 4:  # Adjust size for muscular thighs
                            if base_size in SIZE_ORDER and SIZE_ORDER.index(base_size) < len(SIZE_ORDER) - 1:
                                base_size = SIZE_ORDER[SIZE_ORDER.index(base_size) + 1]
                                logging.info(f"Size adjusted to {base_size} for muscular thighs")  # Log size adjustment
                                
                elif choice in ['2', '4']:  # Handle pants or dress
                    age = get_age_input("Enter your age")  # Get age
                
                # Show results
                sizes = show_size_range(base_size, clothing_type, gender)  # Show size range
                uk_size = convert_to_uk(base_size, clothing_type, gender)  # Convert to UK size
                display_size_recommendation(
                    clothing_type, 
                    gender if clothing_type != CLOTHING_TYPES.DRESS.name.lower() else None,
                    age if choice != '1' else None, 
                    base_size, 
                    uk_size
                )  # Display final recommendation
                
                # Continue prompt
                while True:  # Loop until valid input is received
                    cont = input("Would you like to check another clothing item? (1:Yes, 0:No): ").strip()  # Get input
                    if cont in ['1', '0']:  # Validate input
                        break
                    print("❌ Invalid input. Please enter 1 or 0.")  # Show error message
                    
                if cont != '1':  # Handle exit
                    print("👋 Thank you for using the UK Size Fit Recommender. Goodbye!")  # Show goodbye message
                    logging.info("Program terminated by user")  # Log user exit
                    break
                    
            except Exception as e:  # Handle errors in clothing type loop
                print(f"❌ An error occurred: {str(e)}")  # Show error message
                logging.error(f"Error in clothing type loop: {str(e)}", exc_info=True)  # Log error with traceback
                continue
                
    except Exception as e:  # Handle errors in main function
        print(f"❌ A critical error occurred: {str(e)}")  # Show error message
        logging.critical(f"Critical error in main function: {str(e)}", exc_info=True)  # Log critical error with traceback
        sys.exit(1)  # Exit with error status

if __name__ == "__main__":
    main()  # Run main function
