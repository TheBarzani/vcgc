from vcgc.network import *

G = VCPNetwork()
G.read_dimacs("dimacs/g000.dimacs")
G.draw_colored_graph()