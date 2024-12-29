import streamlit as st

# Title
st.title("Minimal Streamlit Test")

# Sidebar Sliders and Button
st.sidebar.header("Test Sidebar")
number = st.sidebar.slider("Pick a Number", 1, 100, 50)
start_button = st.sidebar.button("Start")

# Main Output
st.write(f"Selected Number: {number}")

if start_button:
    st.write("Button Clicked!")
else:
    st.write("Click the button to start.")
