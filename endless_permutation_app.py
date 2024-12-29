import streamlit as st
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

# Title
st.title("Logistic Map-Inspired Permutations with Local Interactions")

# Sidebar Header
st.sidebar.header("General Settings")
iterations = st.sidebar.slider("Number of Iterations", 10, 500, 100, step=10)

# Main Area for Parameters
st.header("Simulation Parameters")
N = st.slider("Number of Elements (N)", 5, 50, 10, step=1)
r = st.slider("Logistic Map Parameter (r)", 0.0, 4.0, 3.8, step=0.01)

# Buttons for Control
col1, col2 = st.columns(2)
run_simulation = col1.button("Run Simulation")
reset_simulation = col2.button("Reset Simulation")

# Session State to Track Simulation State
if "simulation_running" not in st.session_state:
    st.session_state.simulation_running = False

# Handle Button Clicks
if run_simulation:
    st.session_state.simulation_running = True

if reset_simulation:
    st.session_state.simulation_running = False

# Main Simulation Logic
if st.session_state.simulation_running:
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

    # Permutation Evolution Visualization
    st.subheader("Permutation Evolution")
    for t, perm in enumerate(permutation_history[:10]):  # Display first 10 iterations for readability
        st.write(f"Iteration {t + 1}: {perm}")
else:
    st.write("Adjust parameters and click 'Run Simulation' to start.")
