from src.io import load_matrix_from_csv
from src.network import create_graph_with_latency_modified

if __name__ == "__main__":
    # Load the matrices back from the CSV files
    loaded_a_matrix = load_matrix_from_csv('../data/network1/a_matrix.csv')
    loaded_b_matrix = load_matrix_from_csv('../data/network1/b_matrix.csv')
    loaded_c_matrix = load_matrix_from_csv('../data/network1/c_matrix.csv')
    print(loaded_c_matrix)

    n = len(loaded_a_matrix)
    G_modified = create_graph_with_latency_modified(n, loaded_a_matrix, loaded_b_matrix,
                                                    loaded_c_matrix)

    print(G_modified.edges(data=True))  # Display the edges with latency function attributes


