import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

def calculate_entropy(arr):
    """Calculate the number of inversions (entropy) in the array."""
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def simulate_system(S, steps, temperature, A):
    """Simulate the system with local interactions and track entropy."""
    N = len(S)
    B = np.setdiff1d(S, A)  # B is always S \ A
    entropy_A_history = []
    entropy_B_history = []
    entropy_S_history = []

    for step in range(steps):
        # Calculate entropy of A, B, and S
        entropy_A = calculate_entropy(A)
        entropy_B = calculate_entropy(B)
        entropy_S = calculate_entropy(S)

        # Record entropy
        entropy_A_history.append(entropy_A)
        entropy_B_history.append(entropy_B)
        entropy_S_history.append(entropy_S)

        # Simulate local interactions (only neighboring swaps in S)
        i = np.random.randint(0, N - 1)  # Choose a random neighbor pair
        j = i + 1
        S_new = S.copy()
        S_new[i], S_new[j] = S_new[j], S_new[i]

        # Calculate change in entropy (ΔH) and energy (ΔE)
        H_old = calculate_entropy(S)
        H_new = calculate_entropy(S_new)
        delta_H = H_new - H_old
        delta_E = -delta_H

        # Boltzmann acceptance probability
        if delta_E <= 0:
            S = S_new
        else:
            if np.random.rand() < np.exp(-delta_E / temperature):
                S = S_new

        # Update B (since S has changed)
        B = np.setdiff1d(S, A)

        # Yield results for live updating
        yield entropy_A_history, entropy_B_history, entropy_S_history, A, B, S

# Streamlit app
st.title("Entropy Evolution Simulation with Local Interactions")
st.write("Simulate the evolution of entropy in subsets A, B, and the global system S.")

# Parameters
N = st.number_input("Size of the system (N)", min_value=100, max_value=10000, value=1000)
max_size_A = st.number_input("Maximum size of subset A", min_value=1, max_value=100, value=10)
steps = st.number_input("Number of simulation steps", min_value=100, max_value=10000, value=1000)
temperature = st.slider("Temperature (T)", 0.1, 10.0, 1.0)

# Initialize the system
S = np.arange(1, N + 1)
np.random.shuffle(S)

# Define subset A (fixed at the start)
A = np.random.choice(S, size=max_size_A, replace=False)

# Start/Stop button
if "running" not in st.session_state:
    st.session_state.running = False

def toggle_simulation():
    st.session_state.running = not st.session_state.running

st.button("Start/Stop Simulation", on_click=toggle_simulation)

# Placeholders for live updating
plot_placeholder_A = st.empty()
plot_placeholder_B = st.empty()
plot_placeholder_S = st.empty()
A_placeholder = st.empty()
B_placeholder = st.empty()
S_placeholder = st.empty()

# Simulation loop
if st.session_state.running:
    for entropy_A_history, entropy_B_history, entropy_S_history, A, B, S in simulate_system(S, steps, temperature, A):
        # Update plots
        plt.figure(figsize=(10, 3))
        plt.plot(entropy_A_history, label="Entropy of A", color="red")
        plt.xlabel("Time Steps")
        plt.ylabel("Entropy")
        plt.title("Evolution of Entropy of A")
        plt.legend()
        plot_placeholder_A.pyplot(plt)

        plt.figure(figsize=(10, 3))
        plt.plot(entropy_B_history, label="Entropy of B", color="blue")
        plt.xlabel("Time Steps")
        plt.ylabel("Entropy")
        plt.title("Evolution of Entropy of B")
        plt.legend()
        plot_placeholder_B.pyplot(plt)

        plt.figure(figsize=(10, 3))
        plt.plot(entropy_S_history, label="Entropy of S", color="green")
        plt.xlabel("Time Steps")
        plt.ylabel("Entropy")
        plt.title("Evolution of Entropy of S")
        plt.legend()
        plot_placeholder_S.pyplot(plt)

        # Update subset displays
        A_placeholder.write(f"### Subset A: {A}")
        B_placeholder.write(f"### Subset B: {B}")
        S_placeholder.write(f"### Global System S: {S}")

        # Pause for live updating
        time.sleep(0.1)

    # Compare entropy of B with and without A
    B_without_A = S  # When A is not present, B is the entire system
    entropy_B_without_A = calculate_entropy(B_without_A)
    entropy_B_with_A = calculate_entropy(B)

    st.write(f"### Subset A: {A}")
    st.write(f"Entropy of B when A is present: {entropy_B_with_A}")
    st.write(f"Entropy of B when A is absent: {entropy_B_without_A}")
    if entropy_B_with_A < entropy_B_without_A:
        st.write("The subset A satisfies the condition: Entropy of B is lower when A is present.")
    else:
        st.write("The subset A does not satisfy the condition.")
