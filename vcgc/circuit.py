# A module to handle state preparation, oracle attachment, and diffusion circuit generations for grover's circuit

import numpy as np
from qiskit import QuantumCircuit

# Create a quantum subcircuit for grover diffusion operator
def create_grover_diffusion_operator(num_qubits: int) -> QuantumCircuit:
    # Create a quantum subcircuit for grover diffusion operator
    grover_diff = QuantumCircuit(num_qubits, name="grover_diffusion")
    grover_diff.h(range(num_qubits))
    grover_diff.x(range(num_qubits))
    grover_diff.h(num_qubits - 1)
    grover_diff.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    grover_diff.h(num_qubits - 1)
    grover_diff.x(range(num_qubits))
    grover_diff.h(range(num_qubits))
    return grover_diff


def uniform_superposition(M, n):
    """
    Creates a quantum circuit that prepares a uniform superposition state over M basis states.
    This function generates a quantum circuit that creates the uniform superposition state:
    (1/√M) * Σ|j⟩ for j from 0 to M-1, using the minimum number of qubits required 
    ($\frac{1}{\sqrt{M}} \sum_{j=0}^{M-1} \ket{j} $).
    The algorithm uses a recursive approach based on the binary representation of M,
    applying controlled rotations and Hadamard gates to achieve the desired amplitudes.
    Args:
        M (int): A positive integer with 2 < M < 2^n, where M is not equal to 2^r 
                for any natural number r. This represents the number of basis states
                in the uniform superposition.
        n (int): The number of qubits to use. Should be at least ceil(log2(M)) to
                accommodate all M states.
    Returns:
        QuantumCircuit: A quantum circuit that prepares the uniform superposition state
                    when applied to the |0⟩^⊗n initial state.
    Note:
        The function assumes M is not a power of 2, as such cases can be handled
        more simply with just Hadamard gates. The circuit uses controlled Y-rotations
        and controlled Hadamard gates to achieve the precise amplitudes required
        for uniform superposition.
    """
    N = [int(x) for x in list(np.binary_repr(M))][::-1]
    k = len(N)
    L = [index for (index, item) in enumerate(N) if item == 1]  # Locations of '1's
    
    qcircuit = QuantumCircuit(n)
    qcircuit.x(L[1:k])
    Mcurrent = 2**(L[0])
    theta = -2*np.arccos(np.sqrt(Mcurrent/M))
    
    if L[0] > 0:  # if M is even
        qcircuit.h(range(L[0]))
        qcircuit.ry(theta, L[1])
        qcircuit.ch(L[1], range(L[0], L[1]), ctrl_state='0')
    
    for m in range(1, len(L) - 1):
        theta = -2*np.arccos(np.sqrt(2**L[m]/(M - Mcurrent)))
        qcircuit.cry(theta, L[m], L[m+1], ctrl_state='0')
        qcircuit.ch(L[m+1], range(L[m], L[m+1]), ctrl_state='0')
        Mcurrent = Mcurrent + 2**(L[m])
    
    # Note: Removed display() call as it requires IPython/Jupyter
    # display(qcircuit.draw('mpl'))
    return qcircuit