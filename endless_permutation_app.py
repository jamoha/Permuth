import streamlit as st
import numpy as np
import random
import math
import time

# Function to calculate inversions (energy)
def calculate_inversions(permutation):
    inversions = 0
    for i in range(len(permutation)):
        for j in range(i + 1, len(permutation)):
            if permutation[i] > permutation[j]:
                inversions += 1
    return inversions

# Function to calculate local energy change (delta E)
def calculate_delta_energy(permutation, i):
    if permutation[i] > permutation[i + 1]:
        return -1  # Removing an inversion
    elif permutation[i] < permutation[i + 1]:
        return 1  # Adding an inversion
    return 0  # No change

# Function to calculate entropy
def calculate_entropy(state_counts, total_steps):
    probabilities = [count / total_steps for count in state_counts if count > 0]
    return -sum(p * math.log(p) for p in probabilities)

# Streamlit app
st.title("Local Transitions Simulation with Boltzmann Distribution")
st.write("Simulate energy and entropy evolution based on local transitions with Boltzmann distribution.")

# User inputs
N = st.slider("Number of integers (N)", min_value=5, max_value=100, value=10, step=1)
T = st.slider("Temperature (T)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
steps = st.slider("Number of simulation steps", min_value=100, max_value=5000, value=1000, step=100)

# Control buttons
start_simulation = st.button("Start Simulation")
stop_simulation = st.button("Stop Simulation")

# Initialize simulation state
simulation_state = {"running": False}
if start_simulation:
    simulation_state["running"] = True
if stop_simulation:
    simulation_state["running"] = False

# Initialize the system
current_permutation = list(range(1, N + 1))  # Ordered state
random.shuffle(current_permutation)  # Start with a random permutation
current_energy = calculate_inversions(current_permutation)

# Initialize variables for tracking
energies = []
state_counts = [0] * (N * (N - 1) // 2 + 1)  # Possible energy levels (0 to max inversions)
entropy_evolution = []

# Streamlit placeholders for real-time updates
energy_chart_placeholder = st.empty()
entropy_chart_placeholder = st.empty()

# Simulation loop
for step in range(steps):
    if not simulation_state["running"]:
        break  # Stop simulation if requested

    # Pick two adjacent elements to swap
    i = random.randint(0, N - 2)  # Ensure i and i+1 are valid indices
    delta_E = calculate_delta_energy(current_permutation, i)

    # Decide whether to accept the swap
    if delta_E <= 0 or random.random() < np.exp(-delta_E / T):
        # Perform the swap
        current_permutation[i], current_permutation[i + 1] = current_permutation[i + 1], current_permutation[i]
        current_energy += delta_E

    # Track energy
    energies.append(current_energy)
    state_counts[current_energy] += 1

    # Calculate entropy
    current_entropy = calculate_entropy(state_counts, step + 1)
    entropy_evolution.append(current_entropy)

    # Update charts every 100 steps
    if step % 100 == 0 or step == steps - 1:
        with energy_chart_placeholder:
            st.line_chart(energies, use_container_width=True)

        with entropy_chart_placeholder:
            st.line_chart(entropy_evolution, use_container_width=True)

        st.write(f"**Step {step + 1}/{steps}**")
        st.write(f"Current Energy: {current_energy}")
        st.write(f"Current Entropy: {current_entropy:.4f}")

        time.sleep(0.1)  # Simulate delay for better visualization

if simulation_state["running"]:
    st.success("Simulation complete!")
