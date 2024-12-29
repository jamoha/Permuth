import streamlit as st
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("Logistic Map-Inspired Permutations with Local Interactions")

# Sidebar for Parameters
st.sidebar.header("Simulation Parameters")
N = st.sidebar.slider("Number of Elements (N)", min_value=5, max_value=50, value=10, step=1)
r = st.sidebar.slider("Logistic Map Parameter (r)", min_value=0.0, max_value=4.0, value=3.8, step=0.01)
iterations = st.sidebar.slider("Number of Iterations", min_value=10, max_value=500, value=100, step=10)

# Initialize Session State
if "simulation_started" not in st.session_state:
    st.session_state.simulation_started = False

# Buttons for Simulation
if st.sidebar.button("Run Simulation"):
    st.session_state.simulation_started = True

if st.sidebar.button("Reset Simulation"):
    st.session_state.simulation_started = False

# Main Simulation Logic
if st.session_state.simulation_started:
    st.subheader("Simulation Running...")

    # Initial Permutation
    permutation = np.arange(1, N + 1)
    st.write(f"Initial Permutation: {permutation}")

    # Store Permutation History
    permutation_history = []

    # Logistic Transformation Function
    def logistic(x, r):
        return r * x * (1 - x)

    # Simulation Loop
    for _ in range(iterations):
        logistic_values = logistic(permutation / N, r)
        for i in range(len(permutation) - 1):
            if logistic_values[i] > logistic_values[i + 1]:
                permutation[i], permutation[i + 1] = permutation[i + 1], permutation[i]
        permutation_history.append(permutation.copy())

    # Entropy Calculation
    unique_permutations = [tuple(p) for p in permutation_history]
    unique_counts = {perm: unique_permutations.count(perm) for perm in set(unique_permutations)}
    probs = np.array(list(unique_counts.values())) / len(permutation_history)
    entropy_value = entropy(probs)

    # Results Display
    st.subheader("Final Permutation")
    st.write(permutation)

    st.subheader("Entropy Value")
    st.write(f"Entropy: {entropy_value:.4f}")

    st.subheader("Permutation Evolution")
    for t, perm in enumerate(permutation_history[:10]):  # Display first 10 iterations for readability
        st.write(f"Iteration {t + 1}: {perm}")
else:
    st.write("Adjust parameters and click 'Run Simulation' to start.")
