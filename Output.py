import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image  # Import the Pillow library


def wrap_labels(text, max_words_per_line=1):
    """Function to wrap text based on number of words"""
    words = text.split()
    # If text is short enough, return as is
    if len(words) <= max_words_per_line:
        return text
    
    # Split into lines of max_words_per_line
    lines = []
    for i in range(0, len(words), max_words_per_line):
        lines.append(' '.join(words[i:i + max_words_per_line]))
    
    return '\n'.join(lines)

def draw_graph_with_path(graph, path, path_number, pos, start, end, total_cost, background_image=None, node_info=None):
    G = nx.Graph()
    
    # Normalize node names
    start = start.strip()
    end = end.strip()
    
    # Add edges to the graph
    for node1, neighbors in graph.edges.items():
        for node2, weight in neighbors.items():
            G.add_edge(node1.strip(), node2.strip(), weight=weight)  # Normalize node names
    
    # Create wrapped labels
    labels = {node: wrap_labels(node) for node in G.nodes()}
    
    # Set figure size based on the background image dimensions
    if background_image:
        img = Image.open(background_image)
        width, height = img.size
        fig, ax = plt.subplots(figsize=(width / 100, height / 100))  # Convert pixels to inches
    else:
        fig, ax = plt.subplots(figsize=(8, 6))  # Default size if no background image

    # Draw the graph
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=250, font_size=7, ax=ax)
    
    # Set background image if provided
    if background_image:
        img = plt.imread(background_image)
        ax.imshow(img, extent=[0, 10, 0, 7], aspect='auto', zorder=0)  # Adjust extent based on your coordinate range
    
    # Set node colors
    node_colors = []
    for node in G.nodes():
        if node == start:
            node_colors.append('green')  # Start node color
        elif node == end:
            node_colors.append('red')  # End node color
        else:
            node_colors.append('lightblue')  # Default color for other nodes
    
    # Redraw the graph with the correct node colors and gray edges
    nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors, node_size=250, font_size=7, ax=ax, edge_color='gray')
    
    # Highlight the path color
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2.5, ax=ax)

    # Annotate edges with weights
    edge_labels = {(node1, node2): weight for node1, neighbors in graph.edges.items() for node2, weight in neighbors.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=5, ax=ax)
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Starting Location',
                   markerfacecolor='green', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Destination',
                   markerfacecolor='red', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Landmarks',
                   markerfacecolor='lightblue', markersize=10),
        plt.Line2D([0], [0], color='gray', label='Pedestrian Network', linewidth=2),
        plt.Line2D([0], [0], color='blue', label='Path', linewidth=2)
    ]

    # Place legend at the bottom of the figure
    ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.1),
              ncol=5, frameon=False)
    
    # Remove axes but keep the legend
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Adjust layout to minimize whitespace
    plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
    
    return fig  # Return the figure instead of showing it

def draw_full_graph(graph, pos, background_image=None):
    G = nx.Graph()
    
    # Add edges to the graph
    for node1, neighbors in graph.edges.items():
        for node2, weight in neighbors.items():
            G.add_edge(node1.strip(), node2.strip(), weight=weight)  # Normalize node names
    
    # Create wrapped labels
    labels = {node: wrap_labels(node) for node in G.nodes()}
    
    # Set fixed limits for the axes
    x_limits = (0, 10)  # Set these based on your coordinate range
    y_limits = (0, 7)   # Set these based on your coordinate range

    # Set figure size based on the background image dimensions
    if background_image:
        img = Image.open(background_image)
        width, height = img.size
        fig, ax = plt.subplots(figsize=(width / 100, height / 100))  # Convert pixels to inches (1 inch = 100 pixels)
    else:
        fig, ax = plt.subplots(figsize=(8, 6))  # Default size if no background image

    # Draw the graph first to set the limits
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=250, font_size=7, ax=ax, edge_color='gray')
    
    # Set background image if provided
    if background_image:
        img = plt.imread(background_image)
        # Adjust extent to fill the entire plot area
        plt.imshow(img, extent=[x_limits[0], x_limits[1], y_limits[0], y_limits[1]], aspect='auto', zorder=0)
    
    # Set node colors
    node_colors = ['lightblue' for _ in G.nodes()]  # Default color for all nodes
    
    # Redraw the graph with the correct node colors
    nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors, node_size=250, font_size=7, ax=ax, edge_color='gray')

    # Annotate edges with weights
    #edge_labels = {(node1, node2): weight for node1, neighbors in graph.edges.items() for node2, weight in neighbors.items()}
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=6, ax=ax)

    # Remove axes
    ax.axis('off')  # Hide the axes

    # Adjust layout to minimize whitespace
    plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
    #plt.show()
    return fig  # Return the figure instead of showing it

def display_paths(sorted_paths, k, paths_with_costs, graph, pos, start, end):
    for i, path in enumerate(sorted_paths, start=1):
        cost = next(cost for p, cost in paths_with_costs if list(p) == list(path))
        print(f"Path {i}: {' -> '.join(path)}, Cost: {cost}")
        draw_graph_with_path(graph, path, i, pos, start, end, cost)

    if len(sorted_paths) < k:
        print("No more paths found.")
