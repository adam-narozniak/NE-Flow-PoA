import itertools
import networkx as nx
import numpy as np
from scipy.optimize import minimize


# The main functionality below will be to iterate over all possible edge combinations
# using itertools
# Example: edges 0 1 2 will create following combinations from itertols:
# 0 1 2
# 0 2 1
# 1 2 0
# 1 0 2
# 2 1 0
# 2 0 1
# In our case if source node = 0 and  target node = 2, we focus only on all paths
# which start at 0 and reach 2, these are:
# 0 1 2
# 0 2
def find_all_paths(G: nx.DiGraph, source_node=None, target_node=None):
    if source_node is None:
        source_node = 0
    if target_node is None:
        target_node = len(G.nodes) - 1
    # In this filter we make sure that first edge in combination starts with our
    # source_node
    # and that there exists a target in destination in any node which (target is the
    # ending node)
    filtered_permutations1 = [
        edges_combination for edges_combination in
        itertools.permutations(G.edges(data=True))
        if edges_combination[0][0] == source_node
           and any(edge[1] == target_node for edge in edges_combination)
    ]
    # In this filter we remove all edges after target node (in destination) was found
    # in destination (Truncate). (We don't need cases like path 0-2 and 1-2. We
    # delete 1-2)
    filtered_permutations2 = []
    for edges_combination in filtered_permutations1:
        for i, edge in enumerate(edges_combination):
            current = edges_combination[:i + 1]
            if edge[1] == target_node:
                filtered_permutations2.append(current)
                break
    # Adding condition to keep grpah connected (src = prev destination. 0-1 and 1-2
    # are connected, while 0-1 and 0-2 are not)
    # And make sure this doesnt happen: 0-1 -> 1-2 -> 2-1. No coming back!
    filtered_permutations3 = [
        combination for combination in filtered_permutations2
        if all(combination[i][1] == combination[i + 1][0] for i in
               range(len(combination) - 1))
           and all(combination[i][0] != combination[i + 1][1] for i in
                   range(len(combination) - 1))
    ]

    # This filter will remove duplicates.
    filtered_permutations4 = []
    for combination in filtered_permutations3:
        if combination not in filtered_permutations4:
            filtered_permutations4.append(combination)

    return filtered_permutations4


def create_latency_fun(paths):
    p_s = {}
    for path_idx, path in enumerate(paths):
        # To start from 1
        # path_idx = path_idx + 1
        value = []
        for edge in path:
            key = (edge[0], edge[1])
            if key not in p_s:
                p_s[key] = [path_idx]
            else:
                p_s[key].append(path_idx)
    return p_s

def find_nash_equilibrium(paths, p_s):
    """
    Finds the socially optimal flow of in a graph 
    G_modified - graph with latency functions
    """
    n  = len(paths)
    f = np.array([0] * n)

    def Latency(x):
        """
        Finds the latency of the graph given the flow
        x - flow in a graph
        """
        L = 0
        for i_path, path in enumerate(paths):
            L_path = 0
            for edge in path:
                a = edge[2]['a']
                b = edge[2]['b']
                c = edge[2]['c']
                p_edge = p_s[(edge[0], edge[1])]
                x_edge = 0
                for i in p_edge:
                    x_edge += x[i]
                L_path += 1/3 * a * x_edge**3 + 1/2 * b * x_edge**2 + c * x_edge
            L += L_path
        return L
        
    start_flow = np.array([1/n]*n)
    bounds = [(0,1)] * n
    cons = ({'type': 'eq', 'fun': lambda x:  sum(x)-1},
        {'type': 'ineq', 'fun': lambda x: x})
    minimum = minimize(Latency, start_flow, bounds=bounds, constraints=cons)
    return minimum.x, minimum.fun 
    
def find_nash_equilibrium2(paths, p_s, edges):
    """
    Finds the socially optimal flow of in a graph 
    G_modified - graph with latency functions
    """
    n  = len(paths)
    f = np.array([0] * n)

    def Latency(x):
        """
        Finds the latency of the graph given the flow
        x - flow in a graph
        """
        L = 0
        for edge in edges:
            a = edge[2]['a']
            b = edge[2]['b']
            c = edge[2]['c']
            p_edge = p_s[(edge[0], edge[1])]
            x_edge = 0
            for i in p_edge:
                x_edge += x[i]
            L += 1/3 * a * x_edge**3 + 1/2 * b * x_edge**2 + c * x_edge
            # L += L_path
        return L
    start_flow = np.array([1/n]*n)
    bounds = [(0,1)] * n
    cons = ({'type': 'eq', 'fun': lambda x:  sum(x)-1},
        {'type': 'ineq', 'fun': lambda x: x})
    minimum = minimize(Latency, start_flow, bounds=bounds, constraints=cons)
    return minimum.x, minimum.fun 

