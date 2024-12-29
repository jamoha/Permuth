import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy

# Title
st.title("Logistic Map-Inspired Permutations with Entropy Evolution")

# Sidebar for Parameters
st.sidebar.header("Simulation Parameters")
N = st.sidebar.slider("Number of Elements (N)", min_value=5, max_value=100, value=10, step=1)
r = st.sidebar.slider("Logistic Map Parameter (r)", min_value=0.0, max_value=4.0, value=3.8, step=0.01)
iterations = st.sidebar.slider("Number of Iterations", min_value=10, max_value=1000, value=100, step=10)

# Buttons
start_simulation = st.sidebar.button("Start Simulation")
reset_simulation = st.sidebar.button("Reset Simulation")

# Session state for managing the simulation
if "simulation_running" not in st.session_state:
    st.session_state.simulation_running = False

# Handle button clicks
if start_simulation:
    st.session_state.simulation_running = True
if reset_simulation:
    st.session_state.simulation_running = False

# Main Simulation Logic
if st.session_state.simulation_running:
    st.subheader("Simulation in Progress...")
    
    # Initialize permutation
    permutation = np.arange(1, N + 1)
    entropy_values = []
    permutation_history = []

    # Define logistic transformation function
    def logistic(x, r):
        return r * x * (1 - x)

    # Create a placeholder for the graph
    entropy_plot = st.empty()
    permutation_display = st.empty()

    # Simulation loop
    for t in range(iterations):
        logistic_values = logistic(permutation / N, r)
        
        # Apply local swaps based on logistic values
        for i in range(len(permutation) - 1):
            if logistic_values[i] > logistic_values[i + 1]:
                permutation[i], permutation[i + 1] = permutation[i + 1], permutation[i]
        
        # Update permutation history
        permutation_history.append(tuple(permutation))
        
        # Calculate current entropy
        unique_permutations, counts = np.unique(permutation_history, axis=0, return_counts=True)
        probs = counts / len(permutation_history)
        current_entropy = entropy(probs)
        entropy_values.append(current_entropy)

        # Update graph and live display
        with entropy_plot.container():
            plt.figure(figsize=(8, 4))
            plt.plot(entropy_values, label="Entropy Evolution", color="blue")
            plt.xlabel("Iteration")
            plt.ylabel("Entropy")
            plt.title("Entropy Evolution")
            plt.legend()
            plt.grid()
            st.pyplot(plt)

        with permutation_display.container():
            st.write(f"Iteration {t + 1}: Current Permutation: {permutation}")

    # Final Results
    st.subheader("Final Results")
    st.write("Final Permutation:", permutation)
    st.write("Final Entropy Value:", entropy_values[-1])
else:
    st.write("Adjust parameters and click **Start Simulation** to begin.")
