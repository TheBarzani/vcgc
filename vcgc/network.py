# This module is to create and visualize NetworkX graphs

import networkx as nx
from matplotlib import pyplot as plt
from vcgc.dimacs import *

class VCPNetwork:
    edges = []
    colored_vertices = {}
    num_vertices = 0
    num_edges = 0
    available_colors = 0
    graph = nx.Graph()  # Declare a graph object
    color_map = []

    def __init__(self):
        pass
    
    def read_dimacs(self, file_path: str) -> None:
        self.num_vertices, self.num_edges, self.available_colors, self.edges, self.colored_vertices = read_dimacs(file_path=file_path)
        self.create_colored_graph(self.num_vertices, self.edges, self.colored_vertices, self.available_colors)

    def create_colored_graph(self, num_vertices: int, edges: list, colored_nodes: dict, num_colors: int,
                              color_map: list = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow']) -> nx.Graph:
        """
        Generate a graph with colored nodes.
        
        Parameters:
        -----------
        num_vertices : int
            Number of vertices in the graph
        edges : list of tuples
            List of edges as (source, target) tuples
        colored_nodes : dict
            Dictionary mapping node IDs (as strings) to color indices (as strings)
        num_colors : int
            Number of available colors
            
        Returns:
        --------
        graph : networkx.Graph
                The generated graph with color attributes embedded in nodes
        """
        
        # Ensure we have enough colors
        if num_colors > len(color_map):
            color_map = color_map * (num_colors // len(color_map) + 1)
        color_map = color_map[:num_colors]
        
        # Create vertices with color attributes
        for v in range(num_vertices):
            # Check if this node has a color assigned
            if str(v) in colored_nodes:
                color_idx = int(colored_nodes[str(v)])
                if 0 <= color_idx < num_colors:
                    # Add node with color attribute directly
                    self.graph.add_node(v, color=color_map[color_idx], color_idx=color_idx)
                else:
                    self.graph.add_node(v, color='lightgray', color_idx=-1)
            else:
                self.graph.add_node(v, color='lightgray', color_idx=-1)
        
        # Add edges
        for e in edges:
            self.graph.add_edge(*e)
        
        return self.graph
    
    def draw_colored_graph(self, figsize: tuple =(5, 5), node_size: int =2000) -> None:
        """
        Draw a graph with nodes colored according to their color attribute.
        Node labels will display both node number and color index in bra-ket notation.
        
        Parameters:
        -----------
        G : networkx.Graph
            The graph to draw (should have 'color' attributes on nodes)
        figsize : tuple, optional
            Figure size as (width, height) in inches
        node_size : int, optional
            Size of the nodes in the visualization
        """
        # Extract node colors for drawing
        node_colors = [self.graph.nodes[node]['color'] for node in self.graph.nodes()]
        
        # Create custom labels in the format "node:|color⟩"
        custom_labels = {}
        for node in self.graph.nodes():
            # Get the color index, default to 'x' if not found or -1
            color_idx = self.graph.nodes[node].get('color_idx', -1)
            if color_idx == -1:
                label = f"{node}"
            else:
                label = f"{node}:|{color_idx}⟩"
            custom_labels[node] = label
        
        # Draw the graph with node colors and custom labels
        plt.figure(figsize=figsize)
        nx.draw(self.graph, labels=custom_labels, node_color=node_colors, node_size=node_size)
        plt.savefig('graph.png', dpi=300, bbox_inches='tight')
        plt.show()