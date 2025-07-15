from vcgc.network import *
from networkx import bfs_tree
import matplotlib.pyplot as plt
import networkx as nx
from vcgc.boolean import BooleanFunction
from tweedledum.synthesis import xag_synth
from tweedledum.qiskit import to_qiskit


network = VCPNetwork()
network.read_dimacs("dimacs/g003.dimacs")
bf = BooleanFunction()
bf.print_vertex_constraints(network)

# Generate the function string (for inspection)
# For single-bit representation (each vertex is 1 bit)
tweedledum_func = bf.create_tweedledum_function(network)

# For multi-bit representation (each vertex uses multiple bits)
tweedledum_func_multibit = bf.create_multi_bit_function(network)

def xag_synthesizer(cf):
    """Custom synthesizer using XAG synthesis instead of PKRM""" 

    # Get the LogicNetwork object from cf.network
    logic_network = cf._logic_network
    
    # Perform XAG synthesis ONCE and store the result
    tweedledum_circuit = xag_synth(logic_network)
    print(f"Number of qubits in Tweedledum circuit: {tweedledum_circuit.num_qubits()}")
    print(tweedledum_circuit)
    qc_qiskit = to_qiskit(tweedledum_circuit, circuit_type="gatelist")

    return qc_qiskit

# Now you can use it with your XAG synthesizer
grover_oracle = xag_synthesizer(tweedledum_func)

