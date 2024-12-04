import streamlit as st
from scipy.stats import hypergeom

# Initialize session state
if "N" not in st.session_state:
    st.session_state["N"] = 60
if "K" not in st.session_state:
    st.session_state["K"] = 24
if "n" not in st.session_state:
    st.session_state["n"] = 7
if "k_input" not in st.session_state:
    st.session_state["k_input"] = "3"
if "result" not in st.session_state:
    st.session_state["result"] = ""

def calculate_probability():
    try:
        N = st.session_state["N"]
        K = st.session_state["K"]
        n = st.session_state["n"]
        k_input = st.session_state["k_input"]

        # Process k input (single value or comma-separated values)
        if ',' in k_input:
            k_values = [int(k.strip()) for k in k_input.split(',')]
        else:
            k_values = [int(k_input)]

        # Compute probabilities
        results = []
        for k in k_values:
            prob = hypergeom.pmf(k, N, K, n) * 100  # Convert to percentage
            results.append(f"P(k={k}) = {prob:.2f}%")

        st.session_state["result"] = "\n".join(results)

    except ValueError:
        st.session_state["result"] = "Please enter valid integer values."

def clear_fields():
    st.session_state["N"] = 60
    st.session_state["K"] = 24
    st.session_state["n"] = 7
    st.session_state["k_input"] = "3"
    st.session_state["result"] = ""

# Streamlit app
st.title("MTG Hypergeometric Calculator")

# Main explanation message
st.markdown(
    """
    ### About This Application
    This code is designed for Magic The Gathering players, but it actually applies to any Trading Card Game.  
    The app computes the probability of drawing a certain number of cards (`k`) out of a certain number of draws (`n`), 
    considering that the deck has `N` total cards and `K` cards of the interested type.

    The algorithm is based on the hypergeometric distribution. Please refer to the Wikipedia page for more details on the math: https://en.wikipedia.org/wiki/Hypergeometric_distribution

    **Example**: You want to know what is the probability to draw 3 lands (`k=3`) in an opening hand (`n=7`) 
    knowing that your deck has `N=60` cards and a total of `K=24` lands.
    """
)

# Input fields
st.header("Enter Parameters Below")
col1, col2 = st.columns(2)
with col1:
    st.number_input("Number of Cards in the Deck (N):", min_value=1, value=st.session_state["N"], key="N")
    st.number_input("Number of Cards of the Chosen Type in the Deck (K):", min_value=1, value=st.session_state["K"], key="K")

with col2:
    st.number_input("Number of Draws (n):", min_value=1, value=st.session_state["n"], key="n")
    st.text_input("How many cards of the chosen type you want to draw? (k):", st.session_state["k_input"], key="k_input")

st.caption("(Enter a single number or a series of numbers separated by commas)")

# Buttons
col1, col2 = st.columns(2)
with col1:
    st.button("Clear Fields", on_click=clear_fields)
with col2:
    st.button("Calculate Probability", on_click=calculate_probability)

# Display results
if st.session_state["result"]:
    st.markdown(f"### Results\n{st.session_state['result']}")

# Footer
st.markdown(
    """
    ---
    **Developed by Federico Tessari, PhD.**  
    Feel free to use it! 😊
    """
)
