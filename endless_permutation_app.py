import streamlit as st
import numpy as np
import random
import pandas as pd
import time
from itertools import permutations

# Define a function to count inversions in a permutation
def count_inversions(permutation):
    inversions = 0
    for i in range(len(permutation)):
        for j in range(i + 1, len(permutation)):
            if permutation[i] > permutation[j]:
                inversions += 1
    return inversions

# Streamlit app
st.title("Live Simulation: Entropy and Permutations")
st.write("Watch the evolution of entropy, energy, and permutations step by step.")

# User inputs
N = st.slider("Number of integers (N)", min_value=2, max_value=10, value=4, step=1)
T = st.slider("Temperature (T)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
steps = st.slider("Number of simulation steps", min_value=10, max_value=200, value=50, step=10)

# Initialize parameters
k_B = 1  # Boltzmann constant
current_permutation = list(range(1, N + 1))  # Start with an ordered permutation
current_energy = count_inversions(current_permutation)

# Initialize trackers
state_counts = {i: 0 for i in range(N * (N - 1) // 2 + 1)}  # Max inversions: N choose 2
entropy_evolution = []
energy_evolution = []
permutation_evolution = []

# Streamlit placeholders
energy_placeholder = st.empty()
entropy_placeholder = st.empty()
permutation_placeholder = st.empty()
chart_placeholder = st.empty()

# Simulation loop
for step in range(steps):
    # Propose a new permutation by swapping two random elements
    new_permutation = current_permutation[:]
    i, j = random.sample(range(N), 2)
    new_permutation[i], new_permutation[j] = new_permutation[j], new_permutation[i]
    new_energy = count_inversions(new_permutation)

    # Metropolis acceptance criterion
    if new_energy < current_energy or random.random() < np.exp(-(new_energy - current_energy) / (k_B * T)):
        current_permutation = new_permutation
        current_energy = new_energy

    # Track permutation, energy, and state counts
    permutation_evolution.append(current_permutation[:])
    energy_evolution.append(current_energy)
    state_counts[current_energy] += 1

    # Calculate probabilities and entropy
    total_visits = sum(state_counts.values())
    current_probs = {E: state_counts[E] / total_visits for E in state_counts if state_counts[E] > 0}
    current_entropy = -k_B * sum(p * np.log(p) for p in current_probs.values())
    entropy_evolution.append(current_entropy)

    # Update live outputs
    energy_placeholder.text(f"Current Energy: {current_energy}")
    entropy_placeholder.text(f"Current Entropy: {current_entropy:.4f}")
    permutation_placeholder.text(f"Current Permutation: {current_permutation}")

    # Update live chart
    with chart_placeholder:
        st.line_chart({"Entropy": entropy_evolution, "Energy": energy_evolution})

    time.sleep(0.1)  # Add delay for live update visualization

st.write("Simulation complete!")
