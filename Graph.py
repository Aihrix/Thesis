from collections import defaultdict

class Graph:
    def __init__(self, graph_dict, travel_times, pos=None):
        self.edges = graph_dict
        self.travel_times = travel_times  # Store travel times
        self.visit_counts = defaultdict(lambda: defaultdict(int))
        self.pos = pos if pos is not None else {}  # Store node positions
        self.nodes = list(graph_dict.keys())


def read_graph_from_files(nodes_filename, edges_filename):
    graph_dict = defaultdict(dict)
    travel_times = defaultdict(dict)  # New dictionary for travel times
    pos = {}

    # Read nodes and coordinates
    with open(nodes_filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):  # Skip empty lines or comments
                continue
            
            # Split line by spaces
            parts = line.split(",")
            if len(parts) == 3:  # Expecting (node x y)
                try:
                    node, x, y = parts
                    pos[node.strip()] = (float(x), float(y))  # Normalize node name
                except ValueError:
                    print(f"Error parsing coordinates for line: {line}")
                    raise

    # Read edges, weights, and travel times
    with open(edges_filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):  # Skip empty lines or comments
                continue
            
            # Split line by spaces
            parts = line.split(",")
            if len(parts) == 4:  # Expecting (node1 node2 weight travel_time)
                try:
                    node1, node2, weight, travel_time = parts
                    graph_dict[node1.strip()][node2.strip()] = int(weight)  # Normalize node names
                    graph_dict[node2.strip()][node1.strip()] = int(weight)  # Assuming undirected graph
                    travel_times[node1.strip()][node2.strip()] = float(travel_time)  # Store travel time as float
                    travel_times[node2.strip()][node1.strip()] = float(travel_time)  # Store travel time as float
                except ValueError:
                    print(f"Error parsing edge for line: {line}")
                    raise

    return graph_dict, travel_times, pos
