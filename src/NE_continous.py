from NE_discrete import all_paths_without_loops, update_edge_flow, \
    calculate_all_latencies


def init_partition(G, paths):
    return [1 / len(paths)] * len(paths)


MIN_DELTA = 1e-6
STOPPING_CONDITION = 1e-7


def compare_latencies(latency, partition):
    non_zero_latencies = []
    for i in range(len(latency)):
        if partition != 0:
            non_zero_latencies.append(latency[i])
    # calculate difference between the fastest and the slowest path
    difference = max(non_zero_latencies) - min(non_zero_latencies)
    return difference


def calculate_nash_flow(G, start_node=None, stop_node=None, max_iter=100000, delta=0.5,
                        lr=1 - 1e-3, eps=1e-6, verbose=False):
    """
    Calculate the Nash flow of a given graph.
    """
    # Initialize the flow of all edges to 0
    if start_node is None:
        start_node = 0
    if stop_node is None:
        stop_node = len(G) - 1
    for edge in G.edges:
        G[edge[0]][edge[1]]["flow"] = 0

    # Find all paths without loops from start_node to stop_node
    paths = all_paths_without_loops(G, start_node, stop_node)

    # Initialize the partition
    partition = init_partition(G, paths)

    # Update the flow of the edges in a given path in a graph
    update_edge_flow(G, paths, partition)
    latencies = None
    # Calculate the Nash flow
    for iteration in range(max_iter):
        for i in range(len(paths)):
            # Calculate the latencies of all paths in a graph
            latencies = calculate_all_latencies(G, paths)

            min_latency = min(latencies)
            min_index = latencies.index(min_latency)

            # If path is already the fastest 
            if latencies[i] <= min_latency:
                continue

            # Update the partition
            if partition[i] != 0:
                diff = partition[i] * delta
                partition[i] -= diff
                partition[i] = 0 if partition[i] < eps else partition[i]
                partition[min_index] += diff

            # Update the flow of the edges in the paths
            update_edge_flow(G, paths, partition)

        if compare_latencies(latencies, partition) < STOPPING_CONDITION:
            if verbose:
                print("Stopping condition reached after ", iteration, " iterations!")
                print("Final latencies: ", latencies)
                print("Final partition: ", partition)
            return G, partition, paths, latencies

        delta = delta * lr
        delta = max(delta, MIN_DELTA)

        # Print the results
        if verbose:
            print("----------------------------------")
            print("Iteration: ", iteration)
            print("Partition: ", partition)
            print("Latencies: ", latencies)
            print("Delta: ", delta)

    final_latencies = calculate_all_latencies(G, paths)
    if verbose:
        print("Max iterations reached!")
        print("Final latencies: ", final_latencies)
        print("Final partition: ", partition)

    return G, partition, paths, final_latencies
