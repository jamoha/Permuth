import streamlit as st
import time

# Function to apply the swapping rule
def apply_rule(seq):
    new_seq = seq[:]
    for i in range(len(seq) - 1):
        if new_seq[i] > new_seq[i + 1]:
            new_seq[i], new_seq[i + 1] = new_seq[i + 1], new_seq[i]
    return new_seq

# Streamlit app
st.title("Live Endless Permutation Simulator")
st.write("Watch the permutations evolve live after an initial flip!")

# User inputs
N = st.slider("Number of elements in the sequence", 5, 20, 10)
steps = st.slider("Number of steps to simulate", 10, 100, 50)
speed = st.slider("Speed (seconds between updates)", 0.1, 1.0, 0.5)

# Initialize sequence and perform an initial disruptive flip
sequence = list(range(1, N + 1))
sequence[1], sequence[-1] = sequence[-1], sequence[1]  # Swap two far-apart numbers

# Run the simulation
if st.button("Run Simulation"):
    st.write("Initial Sequence:")
    st.write(sequence)
    
    # Placeholder for live updates
    placeholder = st.empty()
    
    for step in range(steps):
        sequence = apply_rule(sequence)
        # Update the placeholder with the current sequence
        placeholder.text(f"Step {step + 1}: {sequence}")
        time.sleep(speed)  # Add delay for animation effect
