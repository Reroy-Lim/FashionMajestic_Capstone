"""
MajestiVision Web Application
============================

A Streamlit-based web application for clothing size recommendations.
Provides user authentication and measurement-based size calculations.

Features:
- User authentication (login/signup)
- Measurement input with validation
- Size calculation using the user_size_version3 module
- Modern, responsive UI with custom styling

# Lecturer's Comments:
# - Good use of Streamlit components and layout
# - Consider adding version number and author information
# - Example: __version__ = '1.0.0', __author__ = 'Your Name'
"""

import os  # Import for file operations
import sys  # Import for system operations
import json  # Import for JSON operations
import logging  # Import for logging operations
import logging.handlers  # Import for logging handlers
import datetime  # Import for timestamp operations
import streamlit as st  # Import Streamlit for web interface

from user_size_version3 import (  # Import size calculation functions
    estimate_base_size,  # For calculating base size
    convert_to_uk,  # For converting to UK sizes
    show_size_range,  # For showing size ranges
    get_gender_input,  # For getting gender input
    get_user_input,  # For getting numerical input
    get_optional_measurement,  # For getting optional measurements
    CLOTHING_TYPES,  # For clothing type constants
    setup_logging  # For logging setup
)

# Initialize logging first
setup_logging(logfile = "web_app.log")  # Set up size calculator logging

# Configure logging for the web application
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')  # Create logs directory
os.makedirs(log_dir, exist_ok=True)  # Ensure logs directory exists

log_file = os.path.join(log_dir, 'web_app.log')  # Define log file path
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

logger = logging.getLogger('web_app')  # Get web app logger
logger.setLevel(logging.INFO)  # Set logging level
logger.addHandler(file_handler)  # Add file handler to logger
logger.addHandler(console_handler)  # Add console handler to logger

# Log application start
logger.info("Web application starting")  # Log startup

# Configure Streamlit page
st.set_page_config(
    page_title="MajestiVision",  # Set page title
    page_icon="👕",  # Set page icon
    layout="centered"  # Set layout type
)  # Configure page settings

# Constants for the web application
PAGES = {  # Define page routes
    "login": "MajestiVision.com.sg/Login",  # Login page route
    "measurements": "MajestiVision.com.sg/Size"  # Measurements page route
}

MEASUREMENT_RANGES = {  # Define measurement ranges
    "bust": ["76-80 cm", "81-85 cm", "86-90 cm", "91-95 cm"],  # Bust measurement ranges
    "hips": ["71-76 cm", "77-81 cm", "82-86 cm", "87-91 cm"],  # Hip measurement ranges
    "sleeve": ["83-89 cm", "90-94 cm", "95-99 cm"],  # Sleeve measurement ranges
    "waist": ["Please select one", "66-70 cm", "71-75 cm", "76-80 cm", "81-85 cm"],  # Waist measurement ranges
    "inseam": ["76-83 cm", "84-88 cm", "89-93 cm"]  # Inseam measurement ranges
}

DEFAULT_HEIGHT = 165  # Default height in cm
DEFAULT_WEIGHT = 60  # Default weight in kg

# Custom exception for validation errors
class ValidationError(Exception):
    """Custom exception for validation errors in the web application."""
    pass

def apply_custom_css() -> None:
    """
    Applies custom CSS styling to the Streamlit application.
    Uses markdown with unsafe HTML to inject custom styles.
    
    Example:
        >>> apply_custom_css()
        # Applies custom styling to the application
    """
    try:
        # Custom CSS with logo as background and no empty containers
        st.markdown("""
        <style>
            .stApp {
                background-image: url("MajestiVision logo.jpeg");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }

            .content-overlay {
                background-color: rgba(255, 255, 255, 0.85);
                border-radius: 10px;
                padding: 2rem;
                margin: 2rem auto;
                max-width: 500px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }

            .welcome-box {
                background-color: white;
                border-radius: 8px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                text-align: center;
            }

            .welcome-text {
                font-size: 1.8rem;
                font-weight: bold;
                color: #4CAF50;
                margin: 0;
            }

            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border-radius: 6px;
                padding: 0.5rem 1rem;
                width: 100%;
                border: none;
                font-weight: bold;
            }

            .stButton>button:hover {
                background-color: #45a049;
            }

            .login-form {
                background-color: white;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            .result-box {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 1.5rem;
                margin-top: 1.5rem;
                background-color: #f5f5f5;
            }
        </style>
        """, unsafe_allow_html=True)  # Apply custom CSS
        logging.debug("Custom CSS applied successfully")  # Log success
        
    except Exception as e:  # Handle any errors
        logging.error(f"Failed to apply custom CSS: {str(e)}")  # Log error
        raise  # Re-raise the exception

def display_header(current_page: str) -> None:
    """
    Displays the header section of the web application.
    
    Args:
        current_page (str): Current page identifier
        
    Example:
        >>> display_header("login")
        # Displays header with navigation and page title
    """
    try:
        if current_page not in PAGES:  # Validate page
            raise ValidationError(f"Invalid page: {current_page}")
            
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; font-size: 0.9rem; color: #666;">
            <div>← →</div>
            <div>Q</div>
            <div>{PAGES[current_page]}</div>
        </div>
        """, unsafe_allow_html=True)  # Display header
        
        logging.debug(f"Header displayed for page: {current_page}")  # Log success
        
    except Exception as e:  # Handle any errors
        logging.error(f"Failed to display header: {str(e)}")  # Log error
        raise  # Re-raise the exception

def validate_login_credentials(username: str, password: str) -> bool:
    """
    Validates login credentials.
    
    Args:
        username (str): Username to validate
        password (str): Password to validate
        
    Returns:
        bool: True if credentials are valid
        
    Example:
        >>> validate_login_credentials("user123", "pass123")
        True
    """
    try:
        if not username or not password:  # Check for empty credentials
            raise ValidationError("Username and password are required")
            
        # TODO: Add actual credential validation against a database
        logging.info(f"Login attempt for user: {username}")  # Log login attempt
        return True  # Return success
        
    except ValidationError as e:  # Handle validation errors
        logging.warning(f"Login validation failed: {str(e)}")  # Log warning
        raise  # Re-raise the exception
    except Exception as e:  # Handle other errors
        logging.error(f"Login validation error: {str(e)}")  # Log error
        raise  # Re-raise the exception

def validate_signup_data(username: str, email: str, password: str, confirm_password: str) -> bool:
    """
    Validates signup form data.
    
    Args:
        username (str): Username to validate
        email (str): Email to validate
        password (str): Password to validate
        confirm_password (str): Password confirmation to validate
        
    Returns:
        bool: True if data is valid
        
    Example:
        >>> validate_signup_data("user123", "user@example.com", "pass123", "pass123")
        True
    """
    try:
        if not all([username, email, password, confirm_password]):  # Check for empty fields
            raise ValidationError("All fields are required")
            
        if password != confirm_password:  # Check password match
            raise ValidationError("Passwords do not match")
            
        # TODO: Add more validation (password strength, email format, etc.)
        logging.info(f"Signup validation successful for user: {username}")  # Log success
        return True  # Return success
        
    except ValidationError as e:  # Handle validation errors
        logging.warning(f"Signup validation failed: {str(e)}")  # Log warning
        raise  # Re-raise the exception
    except Exception as e:  # Handle other errors
        logging.error(f"Signup validation error: {str(e)}")  # Log error
        raise  # Re-raise the exception

def login_page() -> None:
    """
    Displays and handles the login page functionality.
    Includes login and signup forms with validation.
    
    Example:
        >>> login_page()
        # Displays login page with forms and handles user input
    """
    try:
        display_header("login")  # Display page header
        
        st.markdown('<div class="content-overlay">', unsafe_allow_html=True)  # Start content overlay
        
        # Display welcome message
        st.markdown("""
        <div class="welcome-box">
            <div class="welcome-text">WELCOME TO<br>MAJESTIVISION</div>
        </div>
        """, unsafe_allow_html=True)  # Show welcome message
        
        # Create login/signup buttons
        col1, col2 = st.columns(2)  # Create two columns
        with col1:  # First column
            if st.button("LOGIN", use_container_width=True, key="login_btn"):  # Login button
                st.session_state.show_login = True  # Show login form
                st.session_state.show_signup = False  # Hide signup form
                logging.debug("Login form selected")  # Log selection
                
        with col2:  # Second column
            if st.button("SIGN-UP", use_container_width=True, key="signup_btn"):  # Signup button
                st.session_state.show_login = False  # Hide login form
                st.session_state.show_signup = True  # Show signup form
                logging.debug("Signup form selected")  # Log selection
        
        # Handle login form
        if st.session_state.get("show_login", True):  # Show login form if selected
            with st.form("login_form"):  # Create login form
                st.markdown('<div class="login-form">', unsafe_allow_html=True)  # Start login form styling
                st.markdown("### Login")  # Form title
                
                # Get login credentials
                username = st.text_input(
                    "Enter Username",
                    placeholder="Enter your username",
                    key="login_username"
                )  # Username input
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )  # Password input
                
                if st.form_submit_button("Login"):  # Handle form submission
                    try:
                        if validate_login_credentials(username, password):  # Validate credentials
                            st.session_state.logged_in = True  # Set logged in state
                            st.session_state.username = username  # Store username
                            st.session_state.page = "measurements"  # Navigate to measurements page
                            logging.info(f"User logged in: {username}")  # Log successful login
                            st.rerun()  # Refresh page
                    except ValidationError as e:  # Handle validation errors
                        st.error(str(e))  # Show error message
                        logging.warning(f"Login failed: {str(e)}")  # Log warning
                    except Exception as e:  # Handle other errors
                        st.error("An error occurred during login")  # Show error message
                        logging.error(f"Login error: {str(e)}")  # Log error
                        
                st.markdown('</div>', unsafe_allow_html=True)  # End login form styling
        
        # Handle signup form
        elif st.session_state.get("show_signup", False):  # Show signup form if selected
            with st.form("signup_form"):  # Create signup form
                st.markdown('<div class="login-form">', unsafe_allow_html=True)  # Start signup form styling
                st.markdown("### Sign Up")  # Form title
                
                # Get signup data
                new_username = st.text_input(
                    "Choose Username",
                    placeholder="Enter a username",
                    key="signup_username"
                )  # Username input
                email = st.text_input(
                    "Email",
                    placeholder="Enter your email",
                    key="signup_email"
                )  # Email input
                new_password = st.text_input(
                    "Create Password",
                    type="password",
                    placeholder="Create a password",
                    key="signup_password"
                )  # Password input
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm your password",
                    key="signup_confirm"
                )  # Password confirmation input
                
                if st.form_submit_button("Sign Up"):  # Handle form submission
                    try:
                        if validate_signup_data(new_username, email, new_password, confirm_password):  # Validate data
                            st.session_state.logged_in = True  # Set logged in state
                            st.session_state.username = new_username  # Store username
                            st.session_state.page = "measurements"  # Navigate to measurements page
                            logging.info(f"New user signed up: {new_username}")  # Log successful signup
                            st.rerun()  # Refresh page
                    except ValidationError as e:  # Handle validation errors
                        st.error(str(e))  # Show error message
                        logging.warning(f"Signup failed: {str(e)}")  # Log warning
                    except Exception as e:  # Handle other errors
                        st.error("An error occurred during signup")  # Show error message
                        logging.error(f"Signup error: {str(e)}")  # Log error
                        
                st.markdown('</div>', unsafe_allow_html=True)  # End signup form styling
        
        st.markdown('</div>', unsafe_allow_html=True)  # End content overlay
        
    except Exception as e:  # Handle any errors
        st.error("An error occurred while displaying the login page")  # Show error message
        logging.error(f"Login page error: {str(e)}")  # Log error
        raise  # Re-raise the exception

def parse_measurement(measurement: str) -> float:
    """
    Parses a measurement string into a float value.
    
    Args:
        measurement (str): Measurement string in format "X-Y cm"
        
    Returns:
        float: Midpoint of the measurement range
        
    Example:
        >>> parse_measurement("76-80 cm")
        78.0
    """
    try:
        # Extract numbers from string
        numbers = [float(x) for x in measurement.split()[0].split('-')]  # Get numbers from string
        if len(numbers) != 2:  # Validate format
            raise ValueError("Invalid measurement format")
            
        # Calculate midpoint
        midpoint = sum(numbers) / 2  # Calculate average
        logging.debug(f"Parsed measurement {measurement} to {midpoint}")  # Log result
        return midpoint  # Return result
        
    except Exception as e:  # Handle any errors
        logging.error(f"Failed to parse measurement {measurement}: {str(e)}")  # Log error
        raise ValueError(f"Invalid measurement format: {measurement}")  # Raise error

def validate_measurements(measurements: dict[str, str]) -> None:
    """
    Validates measurement selections.
    
    Args:
        measurements (dict): Dictionary of measurements
        
    Example:
        >>> validate_measurements({"waist": "Please select one"})
        ValidationError: Please select a waist measurement
    """
    try:
        # Check waist measurement
        if measurements["waist"] == "Please select one":  # Check required measurement
            raise ValidationError("Please select a waist measurement")
            
        # Validate all measurements are in correct format
        for name, value in measurements.items():  # Check each measurement
            if name != "waist" or value != "Please select one":  # Skip waist placeholder
                try:
                    parse_measurement(value)  # Try to parse measurement
                except ValueError:  # Handle parsing errors
                    raise ValidationError(f"Invalid {name} measurement format: {value}")
                    
        logging.debug("Measurements validated successfully")  # Log success
        
    except Exception as e:  # Handle any errors
        logging.error(f"Measurement validation failed: {str(e)}")  # Log error
        raise  # Re-raise the exception

def calculate_size_recommendation(measurements: dict[str, float]) -> tuple[str, str, tuple[str, str, str]]:
    """
    Calculates size recommendation based on measurements.
    
    Args:
        measurements (dict): Dictionary of measurements
        
    Returns:
        tuple: (base_size, uk_size, size_range)
        
    Example:
        >>> calculate_size_recommendation({"bust": 78.0, "waist": 68.0})
        ('M', 'UK 12', ('S', 'M', 'L'))
    """
    try:
        # Calculate base size
        base_size = estimate_base_size(
            height=DEFAULT_HEIGHT,  # Use default height
            weight=DEFAULT_WEIGHT,  # Use default weight
            chest=measurements["bust"],  # Use bust measurement
            waist=measurements["waist"],  # Use waist measurement
            clothing_type=CLOTHING_TYPES.TSHIRT.name.lower()  # Use T-shirt type
        )  # Calculate size
        
        # Convert to UK size
        uk_size = convert_to_uk(
            base_size,
            CLOTHING_TYPES.TSHIRT.name.lower(),
            "female"
        )  # Convert size
        
        # Get size range
        size_range = show_size_range(
            base_size,
            CLOTHING_TYPES.TSHIRT.name.lower(),
            "female"
        )  # Get range
        
        logging.info(f"Size calculation: {base_size} ({uk_size})")  # Log result
        return base_size, uk_size, size_range  # Return results
        
    except Exception as e:  # Handle any errors
        logging.error(f"Size calculation failed: {str(e)}")  # Log error
        raise  # Re-raise the exception

def measurements_page() -> None:
    """
    Displays and handles the measurements page functionality.
    Collects measurements and displays size recommendations.
    
    Example:
        >>> measurements_page()
        # Displays measurements form and calculates size
    """
    try:
        display_header("measurements")  # Display page header
        
        st.markdown('<div class="content-overlay">', unsafe_allow_html=True)  # Start content overlay
        
        st.markdown("### Size Measurement")  # Page title
        st.markdown("To assist you in finding the right clothes, please select your measurement range for the following:")  # Instructions
        
        with st.form("measurements_form"):  # Create measurements form
            # Create two columns for measurements
            col1, col2 = st.columns(2)  # Split into columns
            
            # First column measurements
            with col1:  # First column
                measurements = {  # Get measurements
                    "bust": st.selectbox(
                        "Bust/Chest",
                        options=MEASUREMENT_RANGES["bust"]
                    ),  # Bust measurement
                    "hips": st.selectbox(
                        "Hips",
                        options=MEASUREMENT_RANGES["hips"]
                    ),  # Hip measurement
                    "sleeve": st.selectbox(
                        "Sleeve length",
                        options=MEASUREMENT_RANGES["sleeve"]
                    )  # Sleeve measurement
                }
            
            # Second column measurements
            with col2:  # Second column
                measurements.update({  # Add more measurements
                    "waist": st.selectbox(
                        "Waist",
                        options=MEASUREMENT_RANGES["waist"]
                    ),  # Waist measurement
                    "inseam": st.selectbox(
                        "Inseam",
                        options=MEASUREMENT_RANGES["inseam"]
                    )  # Inseam measurement
                })
            
            st.caption("*Measurements are in cm")  # Add units note
            
            if st.form_submit_button("Calculate Size"):  # Handle form submission
                try:
                    # Validate measurements
                    validate_measurements(measurements)  # Check measurements
                    
                    # Parse measurements
                    parsed_measurements = {  # Convert to numbers
                        name: parse_measurement(value)
                        for name, value in measurements.items()
                        if name != "waist" or value != "Please select one"
                    }  # Parse each measurement
                    
                    # Calculate size
                    base_size, uk_size, (lower, _, upper) = calculate_size_recommendation(
                        parsed_measurements
                    )  # Get size recommendation
                    
                    # Display results
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)  # Start results box
                    st.markdown("### 📏 Size Recommendation")  # Results title
                    st.markdown(f"**Your recommended size:** {base_size} ({uk_size})")  # Show main size
                    st.markdown(
                        f"**May also fit:** {lower}-{upper} "
                        f"({convert_to_uk(lower, 'tshirt', 'female')}-"
                        f"{convert_to_uk(upper, 'tshirt', 'female')})"
                    )  # Show size range
                    st.markdown('</div>', unsafe_allow_html=True)  # End results box
                    
                    logging.info("Size recommendation displayed successfully")  # Log success
                    
                except ValidationError as e:  # Handle validation errors
                    st.error(str(e))  # Show error message
                    logging.warning(f"Measurement validation failed: {str(e)}")  # Log warning
                except Exception as e:  # Handle other errors
                    st.error("An error occurred while calculating your size")  # Show error message
                    logging.error(f"Size calculation error: {str(e)}")  # Log error
        
        st.markdown('</div>', unsafe_allow_html=True)  # End content overlay
        
    except Exception as e:  # Handle any errors
        st.error("An error occurred while displaying the measurements page")  # Show error message
        logging.error(f"Measurements page error: {str(e)}")  # Log error
        raise  # Re-raise the exception

def main() -> None:
    """
    Main function that initializes and runs the web application.
    Sets up session state and handles page routing.
    
    Example:
        >>> main()
        # Initializes and runs the web application
    """
    try:
        # Apply custom styling
        apply_custom_css()  # Apply custom CSS
        
        # Initialize session state
        if "page" not in st.session_state:  # Check if page state exists
            st.session_state.page = "login"  # Set initial page
            st.session_state.logged_in = False  # Set initial login state
            st.session_state.show_login = True  # Show login form by default
            st.session_state.show_signup = False  # Hide signup form by default
            logging.info("Session state initialized")  # Log initialization
            
        # Route to appropriate page
        if st.session_state.page == "login":  # Check if on login page
            if st.session_state.logged_in:  # Check if logged in
                st.session_state.page = "measurements"  # Navigate to measurements
                st.rerun()  # Refresh page
            else:
                login_page()  # Show login page
                
        elif st.session_state.page == "measurements":  # Check if on measurements page
            if not st.session_state.logged_in:  # Check if not logged in
                st.session_state.page = "login"  # Navigate to login
                st.rerun()  # Refresh page
            else:
                measurements_page()  # Show measurements page
                
        else:  # Handle unknown page
            logging.error(f"Unknown page: {st.session_state.page}")  # Log error
            st.session_state.page = "login"  # Reset to login page
            st.rerun()  # Refresh page
            
    except Exception as e:  # Handle any errors
        logging.critical(f"Application error: {str(e)}", exc_info=True)  # Log critical error
        st.error("An unexpected error occurred. Please try again later.")  # Show error message
        
if __name__ == "__main__":
    main()  # Run application
