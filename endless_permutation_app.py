import streamlit as st
import numpy as np
import random
import math

# App Title
st.title("Entropy and Energy Simulation")

# Sidebar for parameters
st.sidebar.header("Simulation Parameters")
N_B = st.sidebar.slider("Number of elements in subsystem B", 5, 50, 10, step=1)
N_A = st.sidebar.slider("Number of elements in subsystem A", 1, N_B, 3, step=1)
steps = st.sidebar.slider("Number of simulation steps", 100, 2000, 500, step=100)
T = st.sidebar.slider("Temperature (T)", 0.1, 10.0, 1.0, step=0.1)

# Buttons for simulation control
if "running" not in st.session_state:
    st.session_state.running = False

if st.sidebar.button("Start Simulation"):
    st.session_state.running = True

if st.sidebar.button("Stop Simulation"):
    st.session_state.running = False

# Function to calculate entropy
def calculate_entropy(state_counts, total_steps):
    probabilities = [count / total_steps for count in state_counts if count > 0]
    return -sum(p * math.log(p) for p in probabilities)

# Function to calculate accessible microstates (restricted by A)
def restricted_microstates(B, A):
    restricted_B = [b for b in B if b not in A]
    return len(restricted_B) * (len(restricted_B) - 1) // 2

# Simulation loop
if st.session_state.running:
    # Initialize variables
    B = list(range(1, N_B + 1))  # Subsystem B
    A = list(range(1, N_A + 1))  # Subsystem A

    global_entropies = []
    energies = []

    state_counts_global = [0] * (N_B * (N_B - 1) // 2 + 1)

    for step in range(steps):
        if not st.session_state.running:
            break

        # Shuffle subsystems
        random.shuffle(B)
        random.shuffle(A)

        # Calculate restricted microstates
        accessible_states = restricted_microstates(B, A)
        state_counts_global[accessible_states] += 1

        # Calculate entropy and energy
        entropy = calculate_entropy(state_counts_global, step + 1)
        energy = N_B - accessible_states

        global_entropies.append(entropy)
        energies.append(energy)

        # Update charts
        st.line_chart(energies, caption="Energy Evolution")
        st.line_chart(global_entropies, caption="Global Entropy Evolution")

    st.session_state.running = False
    st.success("Simulation complete!")
