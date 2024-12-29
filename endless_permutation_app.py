import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_entropy(arr):
    """Calculate the number of inversions (entropy) in the array."""
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def simulate_entropy(N, steps, temperature):
    """Simulate the system and track entropy over time using Boltzmann acceptance."""
    # Initialize the set
    S = np.arange(1, N + 1)
    entropy_history = [calculate_entropy(S)]

    for _ in range(steps):
        # Randomly choose two elements to swap
        i, j = np.random.choice(N, 2, replace=False)
        S_new = S.copy()
        S_new[i], S_new[j] = S_new[j], S_new[i]

        # Calculate change in entropy (ΔH) and energy (ΔE)
        H_old = calculate_entropy(S)
        H_new = calculate_entropy(S_new)
        delta_H = H_new - H_old
        delta_E = -delta_H

        # Boltzmann acceptance probability
        if delta_E <= 0:
            # Always accept if entropy increases (energy decreases)
            S = S_new
        else:
            # Accept with probability exp(-ΔE / T)
            if np.random.rand() < np.exp(-delta_E / temperature):
                S = S_new

        # Record entropy
        entropy_history.append(calculate_entropy(S))

    return entropy_history

# Streamlit app
st.title("Entropy Simulation with Boltzmann Acceptance")
st.write("Simulating a system where entropy evolves based on Boltzmann distribution.")

# Parameters
N = st.slider("Size of the set (N)", 10, 100, 50)
steps = st.slider("Number of simulation steps", 100, 1000, 500)
temperature = st.slider("Temperature (T)", 0.1, 10.0, 1.0)

# Run simulation
entropy_history = simulate_entropy(N, steps, temperature)

# Plot results
st.write("### Entropy Over Time")
plt.figure(figsize=(10, 6))
plt.plot(entropy_history, label="Entropy")
plt.xlabel("Time Steps")
plt.ylabel("Entropy (Number of Inversions)")
plt.title(f"Evolution of Entropy (Temperature = {temperature})")
plt.legend()
st.pyplot(plt)
