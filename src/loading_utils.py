import csv
import networkx as nx

from network import create_graph_from_matrices


def load_matrix_from_csv(filename):
    matrix = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert back empty strings to 'None'
            cleaned_row = [None if element == "" else float(element) for element in row]
            matrix.append(cleaned_row)
    return matrix


def create_graph(directory_name: str) -> nx.DiGraph:
    """Create graph with latency functions on edges based on adjacency matrices."""
    a_matrix = load_matrix_from_csv(directory_name + '/a_matrix.csv')
    b_matrix = load_matrix_from_csv(directory_name + '/b_matrix.csv')
    c_matrix = load_matrix_from_csv(directory_name + '/c_matrix.csv')
    G = create_graph_from_matrices(a_matrix, b_matrix, c_matrix)
    return G
