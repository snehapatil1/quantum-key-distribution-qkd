### Eavesdropping Simulation

import random
from qiskit import QuantumCircuit, Aer, execute
from qkd.bb84 import generate_bits_and_bases, encode_qubit, measure_qubit

def intercept_and_measure(bit, alice_basis, eve_basis):
    """
        Eve intercepts the qubit, measures it in a random basis, and resends
    """
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if alice_basis == 'X':
        qc.h(0)
    if eve_basis == 'X':
        qc.h(0)
    qc.measure(0, 0)

    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1, memory=True)
    result = int(job.result().get_memory()[0])
    return result

def run_bb84_with_eve(n=100):
    """
        Run the BB84 protocol with an eavesdropper (Eve) intercepting qubits
        Returns:
            - Alice's key
            - Bob's key (corrupted by Eve)
            - Matching indices
            - Error rate due to Eve's interference
    """

    alice_bits, alice_bases = generate_bits_and_bases(n)
    bob_bases = [random.choice(['Z', 'X']) for _ in range(n)]
    eve_bases = [random.choice(['Z', 'X']) for _ in range(n)]
    bob_results = []

    backend = Aer.get_backend('qasm_simulator')

    for i in range(n):
        intercepted_bit = intercept_and_measure(alice_bits[i], alice_bases[i], eve_bases[i])
        qc = encode_qubit(intercepted_bit, eve_bases[i])
        qc = measure_qubit(qc, bob_bases[i])
        job = execute(qc, backend, shots=1, memory=True)
        result = job.result().get_memory()[0]
        bob_results.append(int(result))

    matching_indices = [i for i in range(n) if alice_bases[i] == bob_bases[i]]
    alice_key = [alice_bits[i] for i in matching_indices]
    bob_key = [bob_results[i] for i in matching_indices]

    errors = sum(1 for a, b in zip(alice_key, bob_key) if a != b)
    error_rate = errors / len(alice_key) if alice_key else 0.0

    return alice_key, bob_key, matching_indices, error_rate
