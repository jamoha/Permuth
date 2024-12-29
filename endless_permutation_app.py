import streamlit as st
import random
import math

# Title
st.title("Subsystem Entropy Simulation")

# Sidebar for parameters
st.sidebar.header("Simulation Parameters")
N_B = st.sidebar.slider("Number of elements in subsystem B", 5, 50, 10, step=1)
N_A = st.sidebar.slider("Number of elements in subsystem A", 1, N_B, 3, step=1)
steps = st.sidebar.slider("Number of simulation steps", 100, 2000, 500, step=100)

# Button to start the simulation
run_simulation = st.button("Run Simulation")

# Function to calculate entropy
def calculate_entropy(state_counts, total_steps):
    probabilities = [count / total_steps for count in state_counts if count > 0]
    return -sum(p * math.log(p) for p in probabilities)

# Function to calculate accessible microstates
def restricted_microstates(B, A):
    restricted_B = [b for b in B if b not in A]
    return len(restricted_B) * (len(restricted_B) - 1) // 2

# Simulation logic
if run_simulation:
    st.write("Simulation started...")

    # Initialize subsystems
    B = list(range(1, N_B + 1))
    A = list(range(1, N_A + 1))

    # Initialize tracking variables
    global_entropies = []
    energies = []
    state_counts_global = [0] * (N_B * (N_B - 1) // 2 + 1)

    # Placeholders for live chart updates
    energy_chart_placeholder = st.empty()
    entropy_chart_placeholder = st.empty()

    # Simulation loop
    for step in range(steps):
        # Shuffle subsystems
        random.shuffle(B)
        random.shuffle(A)

        # Calculate restricted microstates
        accessible_states = restricted_microstates(B, A)
        state_counts_global[accessible_states] += 1

        # Calculate entropy and energy
        entropy = calculate_entropy(state_counts_global, step + 1)
        energy = N_B - accessible_states

        # Track results
        global_entropies.append(entropy)
        energies.append(energy)

        # Update charts every 100 steps or at the final step
        if step % 100 == 0 or step == steps - 1:
            with energy_chart_placeholder.container():
                st.subheader("Energy Evolution")
                st.line_chart(energies)

            with entropy_chart_placeholder.container():
                st.subheader("Global Entropy Evolution")
                st.line_chart(global_entropies)

    # Final results
    st.success("Simulation complete!")
    st.write("### Final Results")
    st.write(f"Global Entropy: {global_entropies[-1]:.4f}")
    st.write(f"Final Energy: {energies[-1]:.4f}")
