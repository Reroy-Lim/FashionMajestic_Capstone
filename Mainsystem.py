from flask import Flask, render_template, redirect, url_for, request, flash, session
import re
import os

# Assuming "System Processing" is a directory where all HTML files are stored
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'System Processing')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = 'your_secret_key_here'  # Needed for session and flash messages

# Mock user database for demonstration
users = {
    'test@example.com': {
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'Password123!',
        'measurements': {}
    }
}

@app.route('/')
def welcome():
    return render_template('Welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists and password matches
        if email in users and users[email]['password'] == password:
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('menu'))  # Redirect to menu page after login
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('Login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        
        # Validation checks
        if not all([first_name, last_name, email, password, confirm_password]):
            flash('All fields are required', 'error')
        elif email in users:
            flash('Email already registered', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif not is_strong_password(password):
            flash('Password must be at least 8 characters with uppercase, lowercase, number, and special character', 'error')
        else:
            # Add user to database
            users[email] = {
                'first_name': first_name,
                'last_name': last_name,
                'password': password,
                'measurements': {}
            }
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('Sign-up.html')

@app.route('/start')
def start():
    return redirect(url_for('welcome'))

@app.route('/menu')
def menu():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    return render_template('Menu.html')

@app.route('/category-dropdown')
def category_dropdown():
    return render_template('Category_Dropdown bar.html')

@app.route('/input-measurement')
def input_measurement():
    return render_template('Input_measurement.html')

@app.route('/menu')
def menu():
    #  You already have this route, but I'm including it for completeness
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    return render_template('Menu.html')

@app.route('/searchbar-filter')
def searchbar_filter():
    return render_template('Searchbar_filter.html')

@app.route('/submit-measurement', methods=['POST'])
def submit_measurement():
    if request.method == 'POST':
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        # Add more fields as they appear in your form

        print(f"Received measurement data: Gender={gender}, Height={height}, Weight={weight}")

        # Here you would typically process the data,
        # e.g., save it to a database, perform calculations, etc.

        # For now, let's just display a confirmation message
        flash('Measurements submitted successfully!', 'success')
        return redirect(url_for('menu')) # Redirect back to the menu or a confirmation page
    else:
        return "Method Not Allowed", 405

def is_strong_password(password):
    """Check if password meets strength requirements"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

if __name__ == '__main__':
    # Ensure template folder exists
    if not os.path.isdir(TEMPLATE_DIR):
        print(f"Warning: Template directory {TEMPLATE_DIR} does not exist!")
        print("Creating directory...")
        os.makedirs(TEMPLATE_DIR, exist_ok=True)
    
    # Check if required HTML files exist
    required_files = ['Welcome.html', 'Login.html', 'Sign-up.html', 'Menu.html']
    missing_files = [f for f in required_files if not os.path.isfile(os.path.join(TEMPLATE_DIR, f))]
    
    if missing_files:
        print(f"Warning: The following HTML files are missing in {TEMPLATE_DIR}:")
        for file in missing_files:
            print(f" - {file}")
    
    app.run(debug=True)
