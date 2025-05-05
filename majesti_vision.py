# Run this code on the terminal, to open the website application
streamlit run majesti_vision.py 

import streamlit as st
from user_size_version3 import (  # or from User_size_version3 import
    estimate_base_size, 
    convert_to_uk, 
    show_size_range,
    get_gender_input, 
    get_user_input, 
    get_optional_measurement
)

# Page configuration
st.set_page_config(
    page_title="MajestiVision",
    page_icon="👕",
    layout="centered"
)

# Custom CSS with logo as background and no empty containers
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("MajestiVision logo.jpeg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .content-overlay {{
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 10px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 500px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}

    .welcome-box {{
        background-color: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }}

    .welcome-text {{
        font-size: 1.8rem;
        font-weight: bold;
        color: #4CAF50;
        margin: 0;
    }}

    .stButton>button {{
        background-color: #4CAF50;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        width: 100%;
        border: none;
        font-weight: bold;
    }}

    .stButton>button:hover {{
        background-color: #45a049;
    }}

    .login-form {{
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}

    .result-box {{
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        background-color: #f5f5f5;
    }}
</style>
""", unsafe_allow_html=True)

def display_header(current_page):
    pages = {
        "login": "MajestiVision.com.sg/Login",
        "measurements": "MajestiVision.com.sg/Size"
    }

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; font-size: 0.9rem; color: #666;">
        <div>← →</div>
        <div>Q</div>
        <div>{pages.get(current_page, 'MajestiVision.com.sg')}</div>
    </div>
    """, unsafe_allow_html=True)

def login_page():
    display_header("login")

    st.markdown('<div class="content-overlay">', unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-text">WELCOME TO<br>MAJESTIVISION</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("LOGIN", use_container_width=True, key="login_btn"):
            st.session_state.show_login = True
            st.session_state.show_signup = False
    with col2:
        if st.button("SIGN-UP", use_container_width=True, key="signup_btn"):
            st.session_state.show_login = False
            st.session_state.show_signup = True

    if st.session_state.get("show_login", True):
        with st.form("login_form"):
            st.markdown('<div class="login-form">', unsafe_allow_html=True)
            st.markdown("### Login")
            username = st.text_input("Enter Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            if st.form_submit_button("Login"):
                if username and password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.page = "measurements"
                    st.rerun()
                else:
                    st.error("Please enter both username and password")
            st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.get("show_signup", False):
        with st.form("signup_form"):
            st.markdown('<div class="login-form">', unsafe_allow_html=True)
            st.markdown("### Sign Up")
            new_username = st.text_input("Choose Username", placeholder="Enter a username", key="signup_username")
            email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
            new_password = st.text_input("Create Password", type="password", placeholder="Create a password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")

            if st.form_submit_button("Sign Up"):
                if new_username and email and new_password and confirm_password:
                    if new_password == confirm_password:
                        st.session_state.logged_in = True
                        st.session_state.username = new_username
                        st.session_state.page = "measurements"
                        st.rerun()
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def measurements_page():
    display_header("measurements")

    st.markdown('<div class="content-overlay">', unsafe_allow_html=True)

    st.markdown("### Size Measurement")
    st.markdown("To assist you in finding the right clothes, please select your measurement range for the following:")

    with st.form("measurements_form"):
        col1, col2 = st.columns(2)

        with col1:
            bust = st.selectbox("Bust/Chest", ["76-80 cm", "81-85 cm", "86-90 cm", "91-95 cm"])
            hips = st.selectbox("Hips", ["71-76 cm", "77-81 cm", "82-86 cm", "87-91 cm"])
            sleeve = st.selectbox("Sleeve length", ["83-89 cm", "90-94 cm", "95-99 cm"])

        with col2:
            waist = st.selectbox("Waist", ["Please select one", "66-70 cm", "71-75 cm", "76-80 cm", "81-85 cm"])
            inseam = st.selectbox("Inseam", ["76-83 cm", "84-88 cm", "89-93 cm"])

        st.caption("*Measurements are in cm")

        if st.form_submit_button("Calculate Size"):
            if waist == "Please select one":
                st.error("Please select a waist measurement")
            else:
                bust_mid = sum(map(int, bust.split()[0].split('-'))) / 2
                waist_mid = sum(map(int, waist.split()[0].split('-'))) / 2
                hips_mid = sum(map(int, hips.split()[0].split('-'))) / 2
                inseam_mid = sum(map(int, inseam.split()[0].split('-'))) / 2
                sleeve_mid = sum(map(int, sleeve.split()[0].split('-'))) / 2

                estimated_height = 165
                estimated_weight = 60

                base_size = estimate_base_size(
                    height=estimated_height,
                    weight=estimated_weight,
                    chest=bust_mid,
                    waist=waist_mid,
                    clothing_type="tshirt"
                )

                uk_size = convert_to_uk(base_size, "tshirt", "female")

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown("### 📏 Size Recommendation")
                st.markdown(f"**Your recommended size:** {base_size} ({uk_size})")

                lower, _, upper = show_size_range(base_size, "tshirt", "female")
                st.markdown(f"**May also fit:** {lower}-{upper} ({convert_to_uk(lower, 'tshirt', 'female')}-{convert_to_uk(upper, 'tshirt', 'female')})")
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def main():
    if "page" not in st.session_state:
        st.session_state.page = "login"
        st.session_state.logged_in = False
        st.session_state.show_login = True
        st.session_state.show_signup = False

    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "measurements":
        measurements_page()

if __name__ == "__main__":
    main()
