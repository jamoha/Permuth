import streamlit as st

st.title("Test Streamlit App")

# Sidebar Parameters
st.sidebar.header("Parameters")
number = st.sidebar.slider("Pick a Number", 1, 100, 50)
button = st.sidebar.button("Click Me")

# Main Output
# st.write(f"Selected Number: {number}")

