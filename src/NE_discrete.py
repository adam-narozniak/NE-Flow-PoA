import networkx as nx

def all_paths_without_loops(graph, start, end, current_path=[]):
    # Initialize the current path
    current_path = current_path + [start]
    
    # Base case: If the current node is the end node, return the path
    if start == end:
        return [current_path]
    
    # Recursive case: Explore neighbors
    paths = []
    for neighbor in graph.neighbors(start):
        # Avoid loops by checking if the neighbor is not in the current path
        if neighbor not in current_path:
            new_paths = all_paths_without_loops(graph, neighbor, end, current_path)
            paths.extend(new_paths)
    
    return paths


def update_edge_flow(G, paths, partition):
    """
    Update the flow of the edges in a given path in a graph.
    """
    for edge in G.edges:
        G[edge[0]][edge[1]]["flow"] = 0
    for j in range(len(paths)):
        path = paths[j]
        for i in range(len(path) - 1):
            G[path[i]][path[i + 1]]["flow"] += partition[j]


def calculate_path_latency(G, path):
    """
    Calculate the latency of a given path in a graph.
    """
    latency = 0
    for i in range(len(path) - 1):
        edge = G[path[i]][path[i + 1]]
        latency += edge["a"] * edge["flow"]**2 + edge["b"] * edge["flow"] + edge["c"]
    return latency


def calculate_all_latencies(G, paths):
    """
    Calculate the latencies of all paths in a graph.
    """
    latencies = []
    for i in range(len(paths)):
        latencies.append(calculate_path_latency(G, paths[i]))
    return latencies


def init_partition(G, paths, num_people):
    partition = [0] * len(paths)
    modulo = num_people % len(paths)
    for i in range(len(paths)):
        partition[i] = num_people // len(paths)
        if i < modulo:
            partition[i] += 1
    return partition


def calculate_nash_flow(G, start_node, stop_node, num_people, max_iter=1000, verbose=False):
    """
    Calculate the Nash flow of a given graph.
    """
    # Initialize the flow of all edges to 0
    for edge in G.edges:
        G[edge[0]][edge[1]]["flow"] = 0
    
    # Find all paths without loops from start_node to stop_node
    paths = all_paths_without_loops(G, start_node, stop_node)
    
    # Initialize the partition
    partition = init_partition(G, paths, num_people)
    
    # Update the flow of the edges in the paths
    update_edge_flow(G, paths, partition)
    
    # Start looking for the flow
    iteration = 0
    while iteration < max_iter:
        iteration += 1
        flow_has_changed = False
        for i in range(len(paths)):
            # Calculate the latency of the path
            latencies = calculate_all_latencies(G, paths)
            min_latency = min(latencies)
            min_index = latencies.index(min_latency)

            # If path is already the fastest 
            if latencies[i] <= min_latency:
                continue

            # Update the partition
            if partition[i] != 0:
                flow_has_changed = True
                partition[i] -= 1
                partition[min_index] += 1
            
            # Update the flow of the edges in the paths
            update_edge_flow(G, paths, partition)
            
            if verbose:
                print("----------------------------------")
                print("Iteration: ", iteration)
                print("Partition: ", partition)
                print("Latencies: ", latencies)

        if not flow_has_changed:
            break

    final_latencies = calculate_all_latencies(G, paths)
    if iteration == max_iter:
        print("Max iterations reached!")
    else:
        print("Nash flow found at iteration: ", iteration)

    print("Final latencies: ", final_latencies)
    print("Final partition: ", partition)
    return G, partition, paths, final_latencies
