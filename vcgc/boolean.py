from vcgc.network import *
from tweedledum.bool_function_compiler.bitvec import BitVec
from tweedledum.bool_function_compiler.bool_function import BoolFunction

class BooleanFunction():
    def __init__(self):
        self.boolean_function = None

    def print_vertex_constraints(self, network: VCPNetwork) -> None:
        edges = list(network.graph.edges())
        for i, e in enumerate(edges):
            if i > 0: 
                print(' ∧ ', end='')
            u, v = e
            print(f'(v{u} != v{v})', end='')
        print('\n')

    def generate_coloring_expression(self, network: VCPNetwork):
        """
        Generate a boolean expression string for graph coloring constraints.
        
        Parameters:
        -----------
        network : VCPNetwork
            The graph network containing vertices and edges
            
        Returns:
        --------
        str : Boolean expression string
        list : Variable order for the expression
        """
        vertices = list(network.graph.nodes())
        edges = list(network.graph.edges())
        
        # Create variable names for each vertex
        var_names = [f"v{vertex}" for vertex in vertices]
        
        # Generate constraint clauses using logical operators
        constraints = []
        for u, v in edges:
            # Use XOR for inequality: (a != b) is equivalent to (a ^ b)
            constraints.append(f"(v{u} ^ v{v})")
        
        # Combine all constraints with AND
        if len(constraints) == 0:
            expression = "1"  # Always true if no edges
        elif len(constraints) == 1:
            expression = constraints[0]
        else:
            expression = " & ".join(constraints)
        
        return expression, var_names

    def create_tweedledum_function(self, network: VCPNetwork):
        """
        Create a tweedledum BoolFunction for the graph coloring problem using expression parsing.
        
        Parameters:
        -----------
        network : VCPNetwork
            The graph network containing vertices and edges
            
        Returns:
        --------
        BoolFunction : Tweedledum boolean function object
        """
        expression, var_order = self.generate_coloring_expression(network)
        
        print(f"Generated expression: {expression}\n")
        print(f"Variable order: {var_order}\n")

        # Create BoolFunction from expression
        return BoolFunction.from_expression(expression, var_order)

    def create_multi_bit_function(self, network: VCPNetwork):
        """
        Create a function for multi-bit color representation.
        This creates a more complex expression handling multi-bit inequalities.
        
        Parameters:
        -----------
        network : VCPNetwork
            The graph network containing vertices and edges
        bits_per_color : int
            Number of bits to represent each color
            
        Returns:
        --------
        BoolFunction : Tweedledum boolean function object
        """
        vertices: list = list(network.graph.nodes())
        edges: list = list(network.graph.edges())
        bits_per_color: int = network.available_colors.bit_length()
        
        # Create variable names for each bit of each vertex
        var_names = []
        for vertex in vertices:
            for bit in range(bits_per_color):
                var_names.append(f"v{vertex}_{bit}")
        
        # Generate constraint clauses
        constraints = []
        for u, v in edges:
            # For multi-bit inequality, we need to check if any bit differs
            bit_diffs = []
            for bit in range(bits_per_color):
                bit_diffs.append(f"(v{u}_{bit} ^ v{v}_{bit})")
            
            # At least one bit must be different
            if len(bit_diffs) == 1:
                constraint = bit_diffs[0]
            else:
                constraint = " | ".join(bit_diffs)
            
            constraints.append(f"({constraint})")
        
        # Combine all constraints with AND
        if len(constraints) == 0:
            expression = "1"
        elif len(constraints) == 1:
            expression = constraints[0]
        else:
            expression = " & ".join(constraints)
        
        print(f"Generated multi-bit expression: {expression}")
        print(f"Variable order: {var_names}")
        
        return BoolFunction.from_expression(expression, var_names)