import streamlit as st
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

# Title
st.title("Logistic Map-Inspired Permutations with Local Interactions")

# Sidebar for Parameters
st.sidebar.header("Simulation Parameters")
N = st.sidebar.slider("Number of Elements (N)", 5, 50, 10, step=1)
r = st.sidebar.slider("Logistic Map Parameter (r)", 0.0, 4.0, 3.8, step=0.01)
iterations = st.sidebar.slider("Number of Iterations", 10, 500, 100, step=10)

# Initialize session state for simulation control
if "simulation_started" not in st.session_state:
    st.session_state.simulation_started = False

# Button to start the simulation
start_simulation = st.sidebar.button("Run Simulation")

# Handle button click
if start_simulation:
    st.session_state.simulation_started = True

# Simulation logic
if st.session_state.simulation_started:
    # Initial permutation
    permutation = np.arange(1, N + 1)
    st.write(f"Initial Permutation: {permutation}")

    # To store permutation history for entropy calculation
    permutation_history = []

    # Logistic-like transformation function
    def logistic(x, r):
        return r * x * (1 - x)

    # Simulation loop
    for t in range(iterations):
        # Apply logistic map locally
        logistic_values = logistic(permutation / N, r)
        for i in range(len(permutation) - 1):
            # Compare and swap based on logistic map value
            if logistic_values[i] > logistic_values[i + 1]:
                permutation[i], permutation[i + 1] = permutation[i + 1], permutation[i]
        
        # Store the current permutation
        permutation_history.append(permutation.copy())

    # Calculate entropy evolution
    unique_permutations = [tuple(p) for p in permutation_history]
    unique_counts = {perm: unique_permutations.count(perm) for perm in set(unique_permutations)}
    probs = np.array(list(unique_counts.values())) / len(permutation_history)
    entropy_values = entropy(probs)

    # Visualization
    st.subheader("Final Permutation")
    st.write(permutation)

    st.subheader("Entropy Expansion Over Iterations")
    plt.figure()
    plt.plot(range(len(permutation_history)), [entropy_values] * len(permutation_history), label="Entropy")
    plt.xlabel("Iterations")
    plt.ylabel("Entropy")
    plt.legend()
    st.pyplot(plt)

    st.subheader("Permutation Evolution")
    for t, perm in enumerate(permutation_history):
        st.write(f"Iteration {t + 1}: {perm}")
