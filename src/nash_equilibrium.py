from cmath import inf
import itertools
import networkx as nx

def find_nash_equilibrium(G: nx.DiGraph):
    nodes = list(G.nodes())
    num_nodes = len(nodes)
    final_node_num = num_nodes - 1
    # Initialize the best path and its weight
    best_path = None
    inf_weight = {'a': inf, 'b': inf, 'c': inf}    
    best_weight = inf_weight 
    # Iterate over all possible edge combinations using itertools
    for edges_combination in itertools.permutations(G.edges(data=True)):
        current_weight = {'a': 0, 'b': 0, 'c': 0}
        prev_dst_node = -1
        for idx, edge in enumerate(edges_combination):
            src, dst, abc = edge
            # We always start from 0 node only
            if idx == 0 and src != 0:
                current_weight = inf_weight
                break
            if final_node_num == dst:
                current_weight = add_edges_weights(current_weight, abc)
                break
            if idx == 0:
                prev_dst_node = dst
            # all should be connected (prev dst connected to current src)
            if idx > 0:
                if prev_dst_node != src:
                    current_weight = inf_weight
                    break
                else:
                    prev_dst_node = dst
            current_weight = add_edges_weights(current_weight, abc)
        # If best weight is bigger than our current weight, then we update our new best weight.
        if is_bigger_weight(best_weight, current_weight):
            best_path = edges_combination
            best_weight = current_weight.copy()
    print()
    print("Best path found is:")
    print(best_path)
    print("Best weights are:")
    print(best_weight)

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

