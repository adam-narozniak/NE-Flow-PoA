from io_1 import load_matrix_from_csv
from network import create_graph_with_latency_modified
import nash_equilibrium as ne
import networkx as nx

if __name__ == "__main__":
    path = 'data/network2/'
    # Load the matrices back from the CSV files
    loaded_a_matrix = load_matrix_from_csv(path + 'a_matrix.csv')
    loaded_b_matrix = load_matrix_from_csv(path + 'b_matrix.csv')
    loaded_c_matrix = load_matrix_from_csv(path + 'c_matrix.csv')
    print(loaded_c_matrix)

    n = len(loaded_a_matrix)
    G_modified = create_graph_with_latency_modified(n, loaded_a_matrix, loaded_b_matrix,
                                                    loaded_c_matrix)

    print(G_modified.edges(data=True))  # Display the edges with latency function attributes

    G2 = ne.solve_graph(G_modified)
    print(G2.edges(data=True))
    print(nx.shortest_path(G2, source=0, target=2, weight='weight'))


