import matplotlib.pyplot as plt
import networkx as nx


def edge_weights_func(G, p_s, flow):
    """
    Amount of flow in every edge in a graph
    G - graph
    p_s - paths that every edge belongs to
    flow - flow
    """
    edge_weights = []
    for edge in G.edges:
        weight = 0
        for path in p_s[edge]:
            weight+=flow[path]
        edge_weights.append(weight)
    return edge_weights

def visualize_flow(G, p_s, flow):
    plt.figure(figsize=(8, 6))
    pos = nx.circular_layout(G)

    edge_weights = edge_weights_func(G, p_s, flow)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000,
            font_size=15, edge_color='gray', width=[edge_weight*5 for edge_weight in edge_weights])
    
    edge_labels = {edge:edge_weights[i] for i,edge in enumerate(G.edges)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title("Graph with the flow visualized", fontsize=20)


    