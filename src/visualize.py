import matplotlib.pyplot as plt
import networkx as nx

# Visualize the graph using NetworkX
def visualize_network(G):
    plt.figure(figsize=(8, 6))

    # Node positions in a circular layout for better visualization
    pos = nx.circular_layout(G)

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000,
            font_size=15, edge_color='gray')

    # Draw edge labels (latency function parameters)
    edge_labels = {(u, v): f"a={d['a']}, b={d['b']}, c={d['c']}" for u, v, d in
                   G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Graph with Quadratic Latency Functions", fontsize=20)
    plt.savefig("./../images/test_network1.jpg")


if __name__ == "__main__":
    from io_1 import load_matrix_from_csv
    from src.network import create_graph_with_latency_modified
    loaded_a_matrix = load_matrix_from_csv('../data/network1/a_matrix.csv')
    loaded_b_matrix = load_matrix_from_csv('../data/network1/b_matrix.csv')
    loaded_c_matrix = load_matrix_from_csv('../data/network1/c_matrix.csv')
    print(loaded_c_matrix)

    n = len(loaded_a_matrix)
    G_modified = create_graph_with_latency_modified(n, loaded_a_matrix, loaded_b_matrix,
                                                    loaded_c_matrix)
    visualize_network(G_modified)