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

st.title("Quantum Key Distribution Simulator")
st.markdown("Simulate a quantum key exchange between Alice and Bob using the BB84 protocol.")
simulate_eve_checkbox = st.checkbox("Simulate Eavesdropper (Eve)?", key="eve_checkbox")

num_bits = st.slider("Number of Qubits", min_value=10, max_value=100, step=1, value=50)

if st.button("Run BB84 Simulation"):
    st.session_state.simulation_run_once = True
    st.session_state.simulate_eve_actual = simulate_eve_checkbox
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

# This block will always be evaluated. UI elements are shown if simulation_run_once is True.
if st.session_state.get('simulation_run_once', False):
    st.success("Simulation Completed")
    st.code(f"Alice's Key: {st.session_state.alice_key_str}")
    st.code(f"Bob's Key:   {st.session_state.bob_key_str}")
    st.code(f"Shared Key (Alice's Key): {st.session_state.shared_key}")
    
    if st.session_state.simulate_eve_actual:
        st.subheader("Error Rate Due to Eve")
    else:
        st.subheader("No eavesdropping simulated")
        
    st.code(f"Error Rate: {st.session_state.error_rate:.2%}")
    st.code(f"Matching Bases: {st.session_state.indices_len}")
    st.code(f"Matching Bits: {st.session_state.matches}")
    st.code(f"Key Match Rate: {st.session_state.match_rate:.2%}")

    # Alice wants to send a secret message
    message_input = st.text_area("Enter a message for Alice to encrypt:", key="message_text_area")

    if st.button("Encrypt and Decrypt Message"):
        retrieved_shared_key = st.session_state.get('shared_key')
        if message_input and retrieved_shared_key:
            # Encrypt the message using Alice's shared key
            encrypted_message = encrypt_message(message_input, retrieved_shared_key)
            # Bob receives the message and decrypts it using the shared key
            decrypted_message = decrypt_message(encrypted_message, retrieved_shared_key)

            st.subheader("Encrypted Message:")
            st.write(encrypted_message)

            st.subheader("Decrypted Message:")
            st.write(decrypted_message)
        elif not message_input:
            st.warning("Please enter a message to encrypt and decrypt.")
        else: # This means shared_key is None or empty
            st.error("Shared key not available. Please run the BB84 simulation first.")
else:
    st.info("Click 'Run BB84 Simulation' to start.")

