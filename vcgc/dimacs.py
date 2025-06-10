# This module contains functions to read and write DIMACS files.

class VCP:
    edges = []
    colored_vertices = {}
    num_vertices = 0
    num_edges = 0
    available_colors = 0

    def __init__(self):
        None
        
    def read(self, file_path: str) -> tuple:
        """
        Reads the DIMACS file for a Vertex Coloring Problem and returns the number of vertices, 
        number of edges, colored vertices, the list of edges, and available colors.
        
        Args:
            file_path (str): The path to the DIMACS file.
            
        Returns:
            tuple: returns a tuple of the number of vertices, number of edges, colored vertices, 
            the list of edges, and available colors.
        """
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith('p edge'):
                parts = line.split()
                self.num_vertices = int(parts[2])
                self.num_edges = int(parts[3])
            elif line.startswith('c'):
                continue
            elif line.startswith('n'):
                parts = line.split()
                node = parts[1]
                color = parts[2]
                self.colored_vertices[node] = color
            elif line.startswith('x colors'):
                parts = line.split()
                self.available_colors = int(parts[2])
            else:
                parts = line.split()
                W = int(parts[1])
                V = int(parts[2])
                self.edges.append((W,V))

        return self.num_vertices, self.num_edges, self.available_colors, self.edges, self.colored_vertices