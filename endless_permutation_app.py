import streamlit as st
import numpy as np
import random
import math

# App Title
st.title("Entropy and Energy Simulation with Constraints")
st.sidebar.header("Simulation Parameters")

# Parameters
N_B = st.sidebar.slider("Number of elements in subsystem B", 5, 100, 10, step=1)
N_A = st.sidebar.slider("Number of elements in subsystem A", 1, N_B, 3, step=1)
steps = st.sidebar.slider("Number of simulation steps", 100, 5000, 1000, step=100)
T = st.sidebar.slider("Temperature (T)", 0.1, 10.0, 1.0, step=0.1)

# Initialize B and A
B = list(range(1, N_B + 1))  # Subsystem B
A = list(range(1, N_A + 1))  # Subsystem A (static for simplicity)

# Function to calculate entropy
def calculate_entropy(state_counts, total_steps):
    probabilities = [count / total_steps for count in state_counts if count > 0]
    return -sum(p * math.log(p) for p in probabilities)

# Function to calculate accessible microstates (restricted by A)
def restricted_microstates(B, A):
    restricted_B = [b for b in B if b not in A]
    return len(restricted_B) * (len(restricted_B) - 1) // 2

# Control buttons
start_simulation = st.button("Start Simulation")
stop_simulation = st.button("Stop Simulation")
resume_simulation = st.button("Resume Simulation")

# Simulation state
simulation_state = {"running": False}
if start_simulation:
    simulation_state["running"] = True
if stop_simulation:
    simulation_state["running"] = False
if resume_simulation:
    simulation_state["running"] = True

# Initialize tracking variables
global_entropies = []
entropies_A = []
entropies_B = []
entropies_B_without_A = []
energies = []
state_counts_global = [0] * (N_B * (N_B - 1) // 2 + 1)
state_counts_B_without_A = [0] * (N_B * (N_B - 1) // 2 + 1)
state_counts_A = [0] * (N_A * (N_A - 1) // 2 + 1)
state_counts_B = [0] * (N_B * (N_B - 1) // 2 + 1)

# Streamlit placeholders for live updates
energy_chart_placeholder = st.empty()
global_entropy_chart_placeholder = st.empty()
entropy_A_chart_placeholder = st.empty()
entropy_B_chart_placeholder = st.empty()
entropy_B_without_A_chart_placeholder = st.empty()

# Simulation loop
for step in range(steps):
    if not simulation_state["running"]:
        break  # Stop simulation if requested

    # Randomly shuffle B
    random.shuffle(B)
    random.shuffle(A)

    # Calculate restricted microstates for B with A constraints
    accessible_states_B_with_A = restricted_microstates(B, A)
    state_counts_global[accessible_states_B_with_A] += 1
    state_counts_B[accessible_states_B_with_A] += 1

    # Calculate microstates for B without A
    state_counts_B_without_A[len(B) * (len(B) - 1) // 2] += 1

    # Calculate microstates for A
    state_counts_A[len(A) * (len(A) - 1) // 2] += 1

    # Calculate entropies
    global_entropy = calculate_entropy(state_counts_global, step + 1)
    entropy_A = calculate_entropy(state_counts_A, step + 1)
    entropy_B = calculate_entropy(state_counts_B, step + 1)
    entropy_B_without_A = calculate_entropy(state_counts_B_without_A, step + 1)

    global_entropies.append(global_entropy)
    entropies_A.append(entropy_A)
    entropies_B.append(entropy_B)
    entropies_B_without_A.append(entropy_B_without_A)

    # Track energy as inverse of accessible states (higher constraints = higher energy)
    energy = N_B - accessible_states_B_with_A
    energies.append(energy)

    # Update live charts every 100 steps
    if step % 100 == 0 or step == steps - 1:
        with energy_chart_placeholder.container():
            st.subheader("Energy Evolution")
            st.line_chart(energies)

        with global_entropy_chart_placeholder.container():
            st.subheader("Global Entropy Evolution")
            st.line_chart(global_entropies)

        with entropy_A_chart_placeholder.container():
            st.subheader("Entropy of Subsystem A")
            st.line_chart(entropies_A)

        with entropy_B_chart_placeholder.container():
            st.subheader("Entropy of Subsystem B")
            st.line_chart(entropies_B)

        with entropy_B_without_A_chart_placeholder.container():
            st.subheader("Entropy of Subsystem B without A")
            st.line_chart(entropies_B_without_A)

# Display final results
if simulation_state["running"] or step == steps - 1:
    st.success("Simulation complete!")
    st.write("### Final Results:")
    st.write(f"Global Entropy: {global_entropies[-1]:.4f}")
    st.write(f"Entropy of A: {entropies_A[-1]:.4f}")
    st.write(f"Entropy of B: {entropies_B[-1]:.4f}")
    st.write(f"Entropy of B without A: {entropies_B_without_A[-1]:.4f}")
    st.write(f"Final Energy: {energies[-1]:.4f}")
