from vcgc.network import *
from vcgc.boolean import BooleanFunction
from tweedledum.synthesis import xag_synth
from tweedledum.qiskit import to_qiskit
from tweedledum.bool_function_compiler.bool_function import BoolFunction


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
grover_oracle = xag_synthesizer(tweedledum_func_multibit)
grover_oracle.draw(output='mpl', filename='testing/grover_oracle.png')

bf.create_manual_verilog(network, "testing/manual_coloring.v")
bf.write_verilog_with_custom_mapping(network, "testing/manual_coloring_custom.v")

cf = BoolFunction.from_verilog_file("testing/manual_coloring.v")
# Now you can use it with your XAG synthesizer
grover_oracle_verilog = xag_synthesizer(cf)
grover_oracle_verilog.draw(output='mpl', filename='testing/grover_oracle_verilog.png')
print(grover_oracle.depth())
print(grover_oracle_verilog.depth())


