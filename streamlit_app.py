### Streamlit App

import streamlit as st
from app.qkd import bb84
from app.qkd.eve import run_bb84_with_eve
from app.qkd.utils import compare_keys
from app.qkd.encryption import encrypt_message, decrypt_message

st.set_page_config(page_title="QKD Simulator", layout="centered")

# Initialize session state variables if they don't exist
if 'simulation_run_once' not in st.session_state:
    st.session_state.simulation_run_once = False
    st.session_state.shared_key = None
    st.session_state.alice_key_str = ""
    st.session_state.bob_key_str = ""
    st.session_state.error_rate = 0.0
    st.session_state.indices_len = 0
    st.session_state.matches = 0
    st.session_state.match_rate = 0.0
    st.session_state.simulate_eve_actual = False
    st.session_state.show_technical_details = False
    st.session_state.slider_used = False
    st.session_state.eve_checkbox_shown = False
    st.session_state.eve_checkbox_value = False

st.title("Quantum Key Distribution Simulator")
st.markdown("Simulate a quantum key exchange between Alice and Bob using the BB84 protocol.")

# 1. Number of Qubits slider
num_bits = st.slider("Number of Qubits", min_value=10, max_value=100, step=1, value=0, key="num_bits_slider")

# Track if slider was used (to show next step)
if 'slider_used' not in st.session_state or not st.session_state.slider_used and num_bits > 0:
    st.session_state.slider_used = True

# 2. Show Eve checkbox only after slider is used
if st.session_state.slider_used:
    eve_checkbox = st.checkbox("Simulate Eavesdropper (Eve)?", key="eve_checkbox")
    st.session_state.eve_checkbox_value = eve_checkbox
    st.session_state.eve_checkbox_shown = True
else:
    st.info("Select the number of qubits to start.")
    eve_checkbox = False
    st.session_state.eve_checkbox_value = False
    st.session_state.eve_checkbox_shown = False

# 3. Show Run Simulation button only after Eve checkbox is shown
if st.session_state.eve_checkbox_shown:
    if st.button("Run BB84 Simulation"):
        st.session_state.simulation_run_once = True
        st.session_state.simulate_eve_actual = st.session_state.eve_checkbox_value
        error_rate_temp = 0.00

        if st.session_state.simulate_eve_actual:
            alice_key, bob_key, indices, error_rate_temp = run_bb84_with_eve(num_bits)
        else:
            alice_key, bob_key, indices = bb84.run_bb84(num_bits)
        st.session_state.shared_key = ''.join(map(str, alice_key))
        matches_temp, match_rate_temp = compare_keys(alice_key, bob_key)
        st.session_state.alice_key_str = ''.join(map(str, alice_key))
        st.session_state.bob_key_str = ''.join(map(str, bob_key))
        st.session_state.error_rate = error_rate_temp
        st.session_state.indices_len = len(indices)
        st.session_state.matches = matches_temp
        st.session_state.match_rate = match_rate_temp
        st.session_state.show_technical_details = False

# 4. Show results and technical details button after simulation
if st.session_state.get('simulation_run_once', False):
    st.code(f"Error Rate: {st.session_state.error_rate:.2%}")
    
    if st.session_state.error_rate <= 0:
        st.success("The key exchange was successful!")
    else:
        st.error("Careful! Eve might be listening.")
    
    if st.button("See technical details"):
        st.session_state.show_technical_details = not st.session_state.show_technical_details
    
    if st.session_state.show_technical_details:
        st.subheader("Technical Details")
        st.code(f"Alice's Key: {st.session_state.alice_key_str}")
        st.code(f"Bob's Key:   {st.session_state.bob_key_str}")
        st.code(f"Error Rate: {st.session_state.error_rate:.2%}")
        st.code(f"Key Match Rate: {st.session_state.match_rate:.2%}")
