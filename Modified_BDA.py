import heapq
from collections import defaultdict

def k_shortest_paths(graph, start, end, k, pos):
    found_paths = set()
    paths_with_costs = []

    def bidirectional_dijkstra():
        forward_heap = [(0, start, [])]
        backward_heap = [(0, end, [])]
        forward_visited = {}
        backward_visited = {}

        while forward_heap and backward_heap:
            # Forward search
            dist, node, path = heapq.heappop(forward_heap)
            if node in backward_visited:
                merged_path = path + backward_visited[node][1][::-1]
                full_path = tuple(merged_path)
                return full_path, dist + backward_visited[node][0]

            if node not in forward_visited:
                forward_visited[node] = (dist, path + [node])
                for neighbor, weight in graph.edges[node].items():
                    travel_time = graph.travel_times[node][neighbor]  # Assume travel_times is a dict like edges
                    total_weight = weight + travel_time  # Combine cost and travel time
                    current_visit_count = graph.visit_counts[node][neighbor]
                    if all(current_visit_count <= graph.visit_counts[node][other] for other in graph.edges[node]):
                        heapq.heappush(forward_heap, (dist + total_weight, neighbor, path + [node]))

            # Backward search
            dist, node, path = heapq.heappop(backward_heap)
            if node in forward_visited:
                merged_path = forward_visited[node][1] + path[::-1]
                full_path = tuple(merged_path)
                return full_path, forward_visited[node][0] + dist

            if node not in backward_visited:
                backward_visited[node] = (dist, path + [node])
                for neighbor, weight in graph.edges[node].items():
                    travel_time = graph.travel_times[node][neighbor]  # Assume travel_times is a dict like edges
                    total_weight = weight + travel_time  # Combine cost and travel time
                    current_visit_count = graph.visit_counts[node][neighbor]
                    if all(current_visit_count <= graph.visit_counts[node][other] for other in graph.edges[node]):
                        heapq.heappush(backward_heap, (dist + total_weight, neighbor, path + [node]))

        return None, None

    def update_visit_counts(path):
        for i in range(len(path) - 1):
            graph.visit_counts[path[i]][path[i + 1]] += 1
            graph.visit_counts[path[i + 1]][path[i]] += 1

    def filter_paths(paths):
        unique_paths = set()
        for path in paths:
            path_tuple = tuple(path)
            unique_paths.add(path_tuple)
        return unique_paths

    for _ in range(k):
        path, cost = bidirectional_dijkstra()
        if path is None:
            break

        update_visit_counts(path)
        paths_with_costs.append((list(path), cost))

    # Filter paths before adding to found_paths
    filtered_paths = filter_paths([p[0] for p in paths_with_costs])

    # Add the filtered paths to found_paths
    found_paths.update(filtered_paths)

    sorted_paths = sorted(filtered_paths, key=lambda p: next(cost for path, cost in paths_with_costs if list(path) == list(p)))

    return sorted_paths, paths_with_costs  # Return both sorted paths and their costs
