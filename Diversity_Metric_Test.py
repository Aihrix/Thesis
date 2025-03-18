from Modified_BDA import k_shortest_paths
from Graph import Graph, read_graph_from_files

def calculate_path_cost(path, graph):
    """Calculate the total cost of a given path."""
    cost = 0
    for i in range(len(path) - 1):
        cost += graph.edges[path[i]][path[i + 1]]  # Assuming graph.edges is a dictionary of edge weights
    return cost

def cost_absolute_difference(main_path, alternative_path, graph):
    """Calculate the absolute difference metric for cost."""
    l_main = calculate_path_cost(main_path, graph)  # Calculate cost of the main path
    l_alt = calculate_path_cost(alternative_path, graph)  # Calculate cost of the alternative path
    if l_main == 0:
        return 0  # Avoid division by zero
    return ((l_alt - l_main) / l_main) * 100

def path_overlap_analysis(path1, path2, graph):
    """Calculate the path overlap metric."""
    shared_edges = set()
    for i in range(len(path1) - 1):
        edge1 = (path1[i], path1[i + 1])
        for j in range(len(path2) - 1):
            edge2 = (path2[j], path2[j + 1])
            if edge1 == edge2 or edge1[::-1] == edge2:  # Check for both directions
                shared_edges.add(edge1)
    l_alt = calculate_path_cost(path2, graph)  # Calculate cost of the alternative path
    if l_alt == 0:
        return 0  # Avoid division by zero
    return (sum(graph.edges[edge[0]][edge[1]] for edge in shared_edges) / l_alt) * 100

def travel_time_absolute_difference(main_path, alternative_path, graph):
    """Calculate the absolute difference metric for travel time."""
    t_main = sum(graph.travel_times[main_path[i]][main_path[i + 1]] for i in range(len(main_path) - 1))
    t_alt = sum(graph.travel_times[alternative_path[i]][alternative_path[i + 1]] for i in range(len(alternative_path) - 1))
    if t_main == 0:
        return 0  # Avoid division by zero
    return ((t_alt - t_main) / t_main) * 100

def detour_factor(main_path, alternative_path, graph):
    """Calculate the detour factor (alternative path length / main path length)."""
    l_main = calculate_path_cost(main_path, graph)
    l_alt = calculate_path_cost(alternative_path, graph)
    if l_main == 0:
        return 0  # Avoid division by zero
    return (l_alt / l_main)

def test_diversity_metrics(sorted_paths, graph):
    """Test the diversity metrics for all pairs of paths and return results."""
    results = []
    total_cd = 0
    total_po = 0
    total_tt_ab = 0
    total_df = 0  # Add total detour factor
    count = 0
    path_metrics = {i: {'cd': 0, 'po': 0, 'tt_ab': 0, 'df': 0, 'count': 0} for i in range(len(sorted_paths))}  # Add df to metrics

    for i in range(len(sorted_paths)):
        for j in range(i + 1, len(sorted_paths)):
            main_path = sorted_paths[i]
            alternative_path = sorted_paths[j]
            cd = cost_absolute_difference(main_path, alternative_path, graph)
            po = path_overlap_analysis(main_path, alternative_path, graph)
            tt_ab = travel_time_absolute_difference(main_path, alternative_path, graph)
            df = detour_factor(main_path, alternative_path, graph)  # Calculate detour factor
            results.append((f"Path {i + 1} vs Path {j + 1}", cd, po, tt_ab, df))  # Add df to results
            
            # Accumulate totals for averages
            total_cd += cd
            total_po += po
            total_tt_ab += tt_ab
            total_df += df  # Add to total
            count += 1
            
            # Update path metrics
            path_metrics[i]['cd'] += cd
            path_metrics[i]['po'] += po
            path_metrics[i]['tt_ab'] += tt_ab
            path_metrics[i]['df'] += df  # Add df to path metrics
            path_metrics[i]['count'] += 1
            path_metrics[j]['cd'] += cd
            path_metrics[j]['po'] += po
            path_metrics[j]['tt_ab'] += tt_ab
            path_metrics[j]['df'] += df  # Add df to path metrics
            path_metrics[j]['count'] += 1

    # Calculate and append average metrics for each path
    for i in range(len(sorted_paths)):
        if path_metrics[i]['count'] > 0:
            avg_path_cd = path_metrics[i]['cd'] / path_metrics[i]['count']
            avg_path_po = path_metrics[i]['po'] / path_metrics[i]['count']
            avg_path_tt_ab = path_metrics[i]['tt_ab'] / path_metrics[i]['count']
            avg_path_df = path_metrics[i]['df'] / path_metrics[i]['count']  # Calculate average df
            results.append((f"Path {i + 1} Averages", avg_path_cd, avg_path_po, avg_path_tt_ab, avg_path_df))  # Add df to averages

    return results
