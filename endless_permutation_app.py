import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

def calculate_entropy(arr):
    """Calculate the number of inversions (entropy) in the array."""
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def find_subset_A(S, max_size_A):
    """Find the subset A that minimizes the entropy of B = S \ A."""
    min_entropy = float('inf')
    best_A = None

    # Iterate over all possible subsets A of size up to max_size_A
    for size_A in range(1, max_size_A + 1):
        for A in combinations(S, size_A):
            B = np.setdiff1d(S, A)
            entropy_B = calculate_entropy(B)
            if entropy_B < min_entropy:
                min_entropy = entropy_B
                best_A = A

    return best_A, min_entropy

# Streamlit app
st.title("Deduce Subset A from Entropy Evolution")
st.write("Find the subset A that minimizes the entropy of B = S \\ A.")

# Parameters
N = st.slider("Size of the system (N)", 5, 20, 10)
max_size_A = st.slider("Maximum size of subset A", 1, 10, 5)

# Initialize the system
S = np.arange(1, N + 1)
np.random.shuffle(S)  # Start with a random permutation

# Find the subset A
best_A, min_entropy = find_subset_A(S, max_size_A)

# Display results
st.write("### System S:")
st.write(S)
st.write("### Subset A (deduced):")
st.write(best_A)
st.write("### Entropy of B = S \\ A:")
st.write(min_entropy)

# Plot the system
st.write("### Visualization of Subsets")
plt.figure(figsize=(10, 2))
plt.bar(range(N), [1 if x in best_A else 0 for x in S], color=['red' if x in best_A else 'blue' for x in S])
plt.xticks(range(N), S)
plt.yticks([])
plt.title("Subset A (Red) and Subset B (Blue)")
st.pyplot(plt)
