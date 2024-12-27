import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to apply the swapping rule
def apply_rule(seq):
    new_seq = seq[:]
    for i in range(len(seq) - 1):
        if new_seq[i] > new_seq[i + 1]:
            new_seq[i], new_seq[i + 1] = new_seq[i + 1], new_seq[i]
    return new_seq

# Function to simulate the process
def simulate_permutations(sequence, steps):
    states = [sequence]
    for _ in range(steps):
        sequence = apply_rule(sequence)
        states.append(sequence)
    return states

# Streamlit app
st.title("Endless Permutation Simulator")
st.write("Visualize endless permutations generated from an initial flip.")

# User inputs
N = st.slider("Number of elements in the sequence", 5, 20, 10)
steps = st.slider("Number of steps to simulate", 10, 100, 50)

# Initialize sequence and perform an initial disruptive flip
sequence = list(range(1, N + 1))
sequence[1], sequence[-1] = sequence[-1], sequence[1]  # Swap two far-apart numbers

# Simulate the process
states = simulate_permutations(sequence, steps)

# Display results
if st.button("Run Simulation"):
    st.write(f"Initial sequence: {states[0]}")
    
    # Visualize each step
    for i, state in enumerate(states):
        st.write(f"Step {i}: {state}")
        
    # Plot the evolution
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, state in enumerate(states):
        ax.plot(range(N), state, label=f"Step {i}")
    ax.set_title("Evolution of Permutations")
    ax.set_xlabel("Position")
    ax.set_ylabel("Value")
    ax.legend()
    st.pyplot(fig)
