### BB84 Protocol Implementation

import random
from qiskit import QuantumCircuit, Aer, execute

def generate_bits_and_bases(n):
    """
        Generate random bits and corresponding measurement bases
        - Bits: 0 or 1
        - Bases: Z (computational) or X (Hadamard)
    """
    bits = [random.randint(0, 1) for _ in range(n)]
    bases = [random.choice(['Z', 'X']) for _ in range(n)]
    return bits, bases

def encode_qubit(bit, basis):
    """
        Encode a classical bit into a quantum state based on the given basis.
    """
    qc = QuantumCircuit(1, 1)
    
    # Apply X gate for bit=1
    if bit == 1:
        qc.x(0)
    
    # Apply Hadamard if using X basis
    if basis == 'X':
        qc.h(0)
    
    return qc

def measure_qubit(qc, basis):
    """
        Measure the qubit using the specified basis.
    """
     # Reverse encoding if measuring in X basis
    if basis == 'X':
        qc.h(0)
    
    qc.measure(0, 0)
    
    return qc

def run_bb84(n=100):
    """
        Run the BB84 protocol for n qubits.
        Returns:
            - Alice's key
            - Bob's key
            - Indices where their bases matched
    """
    alice_bits, alice_bases = generate_bits_and_bases(n)
    bob_bases = [random.choice(['Z', 'X']) for _ in range(n)]
    bob_results = []

    backend = Aer.get_backend('qasm_simulator')

    for i in range(n):
        qc = encode_qubit(alice_bits[i], alice_bases[i])
        qc = measure_qubit(qc, bob_bases[i])
        job = execute(qc, backend, shots=1, memory=True)
        result = job.result().get_memory()[0]
        bob_results.append(int(result))

    # Compare only bits where bases matched
    matching_indices = [i for i in range(n) if alice_bases[i] == bob_bases[i]]
    alice_key = [alice_bits[i] for i in matching_indices]
    bob_key = [bob_results[i] for i in matching_indices]

    return alice_key, bob_key, matching_indices
