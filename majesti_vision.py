import streamlit as st
from user_size_version3 import (
    estimate_base_size, convert_to_uk, show_size_range,
    get_gender_input, get_user_input, get_optional_measurement
)

# --- App Config ---
st.set_page_config(page_title="MajestiVision", page_icon="👗")

# --- Mock Login Page ---
def login_page():
    st.title("MajestiVision")
    st.subheader("Login")
    username = st.text_input("Enter Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        st.session_state.logged_in = True
        st.session_state.page = "measurements"
    
    st.write("Or")
    if st.button("Login with Google", type="secondary"):
        st.session_state.logged_in = True
        st.session_state.page = "measurements"
    
    if st.button("Don't have an account? Sign up"):
        st.session_state.page = "signup"

# --- Size Measurement Page ---
def measurements_page():
    st.title("Size Measurement")
    st.write("To assist you in finding the right clothes, please provide your measurements:")
    
    clothing_type = st.selectbox(
        "Clothing Type",
        ["T-shirt", "Long Pants", "Short Pants", "Dress"]
    ).lower().replace(" ", "-")
    
    height = st.number_input("Height (cm)", min_value=100, max_value=250, step=0.1)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, step=0.1)
    gender = get_gender_input(clothing_type)
    
    # Optional measurements
    with st.expander("Advanced Measurements (Optional)"):
        chest = st.number_input("Bust/Chest (cm)", min_value=60, max_value=184, step=1)
        waist = st.number_input("Waist (cm)", min_value=60, max_value=184, step=1)
    
    if st.button("Calculate My Size"):
        base_size = estimate_base_size(height, weight, chest, waist, clothing_type)
        uk_size = convert_to_uk(base_size, clothing_type, gender)
        st.success(f"**Recommended Size:** {base_size} ({uk_size})")

# --- Main App Flow ---
def main():
    if "page" not in st.session_state:
        st.session_state.page = "login"  # Start with login
    
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "measurements":
        measurements_page()

if __name__ == "__main__":
    main()
