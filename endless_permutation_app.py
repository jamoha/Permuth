import streamlit as st
import time

# Function to apply the cyclic disruption rule
def disrupt_sequence(seq, step):
    new_seq = seq[:]
    # Swap two elements based on the step count
    i = step % len(new_seq)
    j = (i + 1) % len(new_seq)  # Wrap around to ensure valid index
    new_seq[i], new_seq[j] = new_seq[j], new_seq[i]
    return new_seq

# Streamlit app
st.title("Deterministic Endless Permutation Simulator")
st.write("Watch deterministic endless permutations evolve live!")

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
    
    # Placeholder for live updates
    placeholder = st.empty()
    
    for step in range(steps):
        sequence = disrupt_sequence(sequence, step)
        
        # Update the placeholder with the current sequence
        placeholder.text(f"Step {step + 1}: {sequence}")
        
        # Add delay for animation effect
        time.sleep(speed)
    
    st.write("Simulation Complete!")
