from vcgc.network import *
from vcgc.boolean import BooleanFunction
from vcgc.synthesis import Synthesizer

def test() -> None:

    network = VCPNetwork()
    network.read_dimacs("dimacs/g006.col")
    network.draw_graph(name="testing/graph.png", node_size=500)
    bf = BooleanFunction()
    bf.print_vertex_constraints(network)

    # For multi-bit representation (each vertex uses multiple bits)
    tweedledum_func_multibit = bf.create_multi_bit_function(network)

    # Testing XAG synthesizer
    synthesizer = Synthesizer(tweedledum_func_multibit)
    synthesizer.synthesize_with_xag()
    synthesizer.print_circuit_info()
    synthesizer.draw_circuit(filename='testing/grover_oracle.png')
    print(f"The circuit depth: {synthesizer.qiskit_circuit.depth()}")

    # Testing with verilog
    # bf.create_manual_verilog(network, "testing/manual_coloring.v")
    # bf.write_verilog_with_custom_mapping(network, "testing/manual_coloring_custom.v")
    # synthesizer.from_verilog_file("testing/manual_coloring.v")
    # synthesizer.synthesize_with_xag()
    # synthesizer.print_circuit_info()
    # synthesizer.draw_circuit(filename='testing/grover_oracle_verilog.png')

if __name__ == "__main__":
    test()


