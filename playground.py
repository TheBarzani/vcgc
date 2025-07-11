from vcgc.network import *
from networkx import bfs_tree
import matplotlib.pyplot as plt
import networkx as nx

G = VCPNetwork()
G.read_dimacs("dimacs/g002.dimacs")
G.draw_colored_graph()
T = bfs_tree(G.graph, source=0)
plt.figure(figsize=[10,10])
nx.draw(T)
plt.savefig('tree.png', dpi=300, bbox_inches='tight')
print(T.edges())