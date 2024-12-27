import streamlit as st
import time

# Function to apply simultaneous neighbor rules
def apply_simultaneous_rule(seq):
    n = len(seq)
    swaps = [False] * n  # Track positions to swap

    # Identify swaps
    for i in range(1, n - 1):
        # Compare with previous neighbor
        if seq[i] < seq[i - 1]:
            swaps[i] = True

        # Compare with next neighbor
        if seq[i] > seq[i + 1]:
            swaps[i + 1] = True

    # Apply all swaps simultaneously
    new_seq = seq[:]
    for i in range(1, n - 1):
        if swaps[i]:
            new_seq[i], new_seq[i - 1] = new_seq[i - 1], new_seq[i]  # Swap with previous
        if swaps[i + 1]:
            new_seq[i + 1], new_seq[i] = new_seq[i], new_seq[i + 1]  # Swap with next

    return new_seq

# Function to calculate the metric (sum of differences of consecutive elements)
def calculate_metric(seq):
    return sum(abs(seq[i] - seq[i - 1]) for i in range(1, len(seq)))

# Streamlit app
st.title("Simultaneous Neighbor Interaction Simulator with Metric")
st.write("Watch permutations evolve with instantaneous neighbor reactions and view the chaos metric!")

# User inputs
N = st.slider("Number of elements in the sequence", 5, 20, 10)
steps = st.slider("Number of steps to simulate", 10, 100, 50)
speed = st.slider("Speed (seconds between updates)", 0.1, 1.0, 0.5)

# Initialize sequence and perform an initial disruptive flip
sequence = list(range(1, N + 1))
sequence[1], sequence[-1] = sequence[-1], sequence[1]  # Initial flip

# Run the simulation
if st.button("Run Simulation"):
    st.write("Initial Sequence:")
    st.write(sequence)
    
    # Placeholders for live updates
    sequence_placeholder = st.empty()
    metric_placeholder = st.empty()
    
    for step in range(steps):
        # Apply the rule
        sequence = apply_simultaneous_rule(sequence)
        
        # Calculate the metric
        metric = calculate_metric(sequence)
        
        # Update the placeholders with the current sequence and metric
        sequence_placeholder.text(f"Step {step + 1}: {sequence}")
        metric_placeholder.text(f"Metric (Sum of Differences): {metric}")
        
        # Add delay for animation effect
        time.sleep(speed)
    
    st.write("Simulation Complete!")
