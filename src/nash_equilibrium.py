from cmath import inf
import itertools
import networkx as nx

def find_all_paths(G: nx.DiGraph, source_node, target_node):
    # nodes = list(G.nodes())
    # num_nodes = len(nodes)
    # final_node_num = num_nodes - 1
    # Initialize the best path and its weight
    best_path = None
    inf_weight = {'a': inf, 'b': inf, 'c': inf}    
    best_weight = inf_weight 
    # Iterate over all possible edge combinations using itertools
    # Example: edges 0 1 2 will create following combinations:
    # 0 1 2 
    # 0 2 1 
    # 1 2 0
    # 1 0 2 
    # 2 1 0  
    # 2 0 1  
    # In our case we focus only on all paths which start at 0 and reach 2, these are:
    # 0 1 2
    # 0 2
    print('-----------------------------------------')
    # This filter will make sure the output of permutation will be not all permutations but only those 
    # which starts with source_node from parameter(first edge has source_node as src) and there is a target_node
    # anywhere as the destination (src->dst) 
    
    # In this filter we make sure that first edge in combination starts with our source_node 
    # and that there exists a destination in any node which is our target (what we look for)
    filtered_permutations1 = [
        edges_combination for edges_combination in itertools.permutations(G.edges(data=True)) 
        if edges_combination[0][0] == source_node
            and any(edge[1] == target_node for edge in edges_combination)
            # and all(edges_combination[i][1] == edges_combination[i + 1][0] for i in range(len(edges_combination) - 2))
    ]
    # In this filter we remove all edges after target node was found in destination. (We don't need cases like path 0-2 and 1-2. We delete 1-2)
    filtered_permutations2 = []
    for edges_combination in filtered_permutations1:
        for i, edge in enumerate(edges_combination):
            current = edges_combination[:i + 1]
            if edge[1] == target_node:
                filtered_permutations2.append(current)
                break
    # Adding condition to keep grpah connected (src = prev destination. 0-1 and 1-2 are connected, while 0-1 and 0-2 are not)
    # And make sure this doesnt happen: 0-1 -> 1-2 -> 2-1. No coming back!
    filtered_permutations3 = [
        combination for combination in filtered_permutations2
        if all(combination[i][1] == combination[i + 1][0] for i in range(len(combination) - 1))
            and all(combination[i][0] != combination[i + 1][1] for i in range(len(combination) - 1))
    ]
    
    # This filter will remove duplicates.
    filtered_permutations4 = []
    for combination in filtered_permutations3:
        if combination not in filtered_permutations4:
            filtered_permutations4.append(combination)
    
    # Just printing out
    for edges_combination in filtered_permutations4:
        prev_dst_node = -1
        print(edges_combination)
        for idx, edge in enumerate(edges_combination):
            src, dst, abc = edge
    return filtered_permutations4
def add_edges_weights(abc_weights1, abc_weights2):
    abc_weights1['a'] = abc_weights1['a'] + abc_weights2['a']
    abc_weights1['b'] = abc_weights1['b'] + abc_weights2['b']
    abc_weights1['c'] = abc_weights1['c'] + abc_weights2['c']
    return abc_weights1

def is_bigger_weight(abc_weights1, abc_weights2):
    if abc_weights1['a'] > abc_weights2['a']:
        return True
    elif abc_weights1['a'] < abc_weights2['a']:
        return False
    else:  # 'a' values are equal, move to 'b'
        if abc_weights1['b'] > abc_weights2['b']:
            return True
        elif abc_weights1['b'] < abc_weights2['b']:
            return False
        else:  # 'b' values are equal, move to 'c'
            return abc_weights1['c'] > abc_weights2['c']

