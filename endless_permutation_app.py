import streamlit as st
import numpy as np
import random
import math

# App Title
st.title("Entropy and Energy Simulation")

# Sidebar for simulation parameters
st.sidebar.header("Simulation Parameters")
N_B = st.sidebar.slider("Number of elements in subsystem B", 5, 50, 10, step=1)
N_A = st.sidebar.slider("Number of elements in subsystem A", 1, N_B, 3, step=1)
steps = st.sidebar.slider("Number of simulation steps", 100, 2000, 500, step=100)
T = st.sidebar.slider("Temperature (T)", 0.1, 10.0, 1.0, step=0.1)

# Buttons for simulation control
start_simulation = st.sidebar.button("Start Simulation")
stop_simulation = st.sidebar.button("Stop Simulation")

# Initialize session state
if "running" not in st.session_state:
    st.session_state.running = False
    st.session_state.step = 0
    st.session_state.results = None

# Button logic
if start_simulation:
    st.session_state.running = True
    st.session_state.step = 0
    st.session_state.results = None

if stop_simulation:
    st.session_state.running = False

# Entropy calculation function
def calculate_entropy(state_counts, total_steps):
    probabilities = [count / total_steps for count in state_counts if count > 0]
    return -sum(p * math.log(p) for p in probabilities)

# Microstates restriction function
def restricted_microstates(B, A):
    restricted_B = [b for b in B if b not in A]
    return len(restricted_B) * (len(restricted_B) - 1) // 2

# Main simulation
if st.session_state.running:
    # Initialize variables
    B = list(range(1, N_B + 1))  # Subsystem B
    A = list(range(1, N_A + 1))  # Subsystem A

    global_entropies = []
    entropies_A = []
    entropies_B = []
    entropies_B_without_A = []
    energies = []

    state_counts_global = [0] * (N_B * (N_B - 1) // 2 + 1)
    state_counts_B_without_A = [0] * (N_B * (N_B - 1) // 2 + 1)
    state_counts_A = [0] * (N_A * (N_A - 1) // 2 + 1)
    state_counts_B = [0] * (N_B * (N_B - 1) // 2 + 1)

    for step in range(st.session_state.step, steps):
        if not st.session_state.running:
            break

        # Randomly shuffle subsystems
        random.shuffle(B)
        random.shuffle(A)

        # Calculate restricted microstates and update state counts
        accessible_states_B_with_A = restricted_microstates(B, A)
        state_counts_global[accessible_states_B_with_A] += 1
        state_counts_B[accessible_states_B_with_A] += 1

        # Microstates for B without A
        state_counts_B_without_A[len(B) * (len(B) - 1) // 2] += 1

        # Microstates for A
        state_counts_A[len(A) * (len(A) - 1) // 2] += 1

        # Entropy calculations
        global_entropy = calculate_entropy(state_counts_global, step + 1)
        entropy_A = calculate_entropy(state_counts_A, step + 1)
        entropy_B = calculate_entropy(state_counts_B, step + 1)
        entropy_B_without_A = calculate_entropy(state_counts_B_without_A, step + 1)

        global_entropies.append(global_entropy)
        entropies_A.append(entropy_A)
        entropies_B.append(entropy_B)
        entropies_B_without_A.append(entropy_B_without_A)

        # Track energy
        energy = N_B - accessible_states_B_with_A
        energies.append(energy)

        # Update live charts every 100 steps
        if step % 100 == 0 or step == steps - 1:
            st.line_chart(energies, caption="Energy Evolution")
            st.line_chart(global_entropies, caption="Global Entropy Evolution")
            st.line_chart(entropies_A, caption="Entropy of Subsystem A")
            st.line_chart(entropies_B, caption="Entropy of Subsystem B")
            st.line_chart(entropies_B_without_A, caption="Entropy of Subsystem B without A")

    # Save results after stopping
    st.session_state.results = {
        "global_entropy": global_entropies[-1] if global_entropies else None,
        "entropy_A": entropies_A[-1] if entropies_A else None,
        "entropy_B": entropies_B[-1] if ent
