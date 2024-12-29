import streamlit as st

# Title
st.title("Basic Streamlit Example")

# Slider
slider_value = st.slider("Select a number", 0, 100, 50)

# Button
if st.button("Show Selected Number"):
    st.write(f"You selected: {slider_value}")
