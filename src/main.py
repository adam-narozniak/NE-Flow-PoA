import timeit
import itertools
from io_1 import load_matrix_from_csv
from network import create_graph_with_latency_modified
import nash_equilibrium as ne

if __name__ == "__main__":
    network_num = 4
    path = 'data/network' + str(network_num) + '/'
    # Load the matrices back from the CSV files
    loaded_a_matrix = load_matrix_from_csv(path + 'a_matrix.csv')
    loaded_b_matrix = load_matrix_from_csv(path + 'b_matrix.csv')
    loaded_c_matrix = load_matrix_from_csv(path + 'c_matrix.csv')
    print(loaded_c_matrix)

    n = len(loaded_a_matrix)
    G_modified = create_graph_with_latency_modified(n, loaded_a_matrix, loaded_b_matrix,
                                                    loaded_c_matrix)

    print(G_modified.edges(data=True))  # Display the edges with latency function attributes
    A = 0
    B = 3
    print(f"All paths from {A} to {B} are presented below:")
    paths = ne.find_all_paths(G_modified, A, B)
    for i, path in enumerate(paths):
        print(f"path {i+1} - {path}")