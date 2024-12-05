import streamlit as st
from scipy.stats import hypergeom

# Initialize session state variables
if "N" not in st.session_state:
    st.session_state["N"] = 60
if "K" not in st.session_state:
    st.session_state["K"] = 24
if "n" not in st.session_state:
    st.session_state["n"] = 7
if "k_input" not in st.session_state:
    st.session_state["k_input"] = "3"
if "result" not in st.session_state:
    st.session_state["result"] = []

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
            # Probability for exactly k
            prob_exact = hypergeom.pmf(k, N, K, n) * 100  # Convert to percentage
            # Cumulative probability for k or less
            prob_cumulative = hypergeom.cdf(k, N, K, n) * 100  # Convert to percentage
            results.append(
                f"The probability to draw **EXACTLY {k}** cards of the chosen type out of {n} draws is: {prob_exact:.2f}%"
            )
            results.append(
                f"The probability to draw {k} cards **OR LESS** of the chosen type out of {n} draws is: {prob_cumulative:.2f}%"
            )
            results.append(
                "---"
            )

        st.session_state["result"] = results

    except ValueError:
        st.session_state["result"] = ["Please enter valid integer values."]

def clear_fields():
    st.session_state["N"] = 60
    st.session_state["K"] = 24
    st.session_state["n"] = 7
    st.session_state["k_input"] = "3"
    st.session_state["result"] = []

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

    In the following you can find some examples.

    **Example 1**: You want to know what is the probability to draw 3 lands (`k=3`) in an opening hand (`n=7`) 
    knowing that your deck has `N=60` cards and a total of `K=24` lands. 

    **Example 2**: You are playing a MTG modern game i.e., the deck has 60 cards. You are at turn 5, and you already drew your opening hand plus 5 other cards because you were on the draw.
    The total number of cards left in your deck are, then, 60-7-5=48. You are running dry on lands since you played only 3 of the 21 lands you have in your deck. This means that in your deck you are left with 18 lands.
    To corerctly decide how to play your next turn, you want to know what is the probability to find one, two or three lands in the next 3 turns i.e., the next 3 draws. In this case you just have to set `N=48`, `K=18`, `k=1,2,3`, `n=3`.
    """
)

# Input fields
st.header("Enter Parameters Below")
col1, col2 = st.columns(2)
with col1:
    st.number_input("Number of Cards in the Deck (N):", min_value=1, key="N")
    st.number_input("Number of Cards of the Chosen Type in the Deck (K):", min_value=1, key="K")

with col2:
    st.number_input("Number of Draws (n):", min_value=1, key="n")
    st.text_input("How many cards of the chosen type you want to draw? (k):", key="k_input")

st.caption("(For 'k' you can either enter a single number or a series of numbers separated by commas)")

# Buttons
col1, col2 = st.columns(2)
with col1:
    st.button("Clear Fields", on_click=clear_fields)
with col2:
    st.button("Calculate Probability", on_click=calculate_probability)

# Display results
if st.session_state["result"]:
    st.markdown("### Results")
    for line in st.session_state["result"]:
        st.write(line)

# Footer
st.markdown(
    """
    ---
    **Developed by Federico Tessari, PhD.**  
    Feel free to use it! 😊
    """
)
