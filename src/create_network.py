import csv
import numpy as np
import random


def save_matrix_to_csv(matrix, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in matrix:
            # Replace 'None' with an empty string for CSV
            cleaned_row = ["" if element is None else element for element in row]
            writer.writerow(cleaned_row)


def create_single_path_matrix(num_edge, randomize=False):
    adj_matrix = np.zeros((num_edge, num_edge), dtype=int)

    # Create top path
    for i in range(num_edge - 1):
        if randomize:
            adj_matrix[i, i + 1] = random.randint(1, 10)
        else:
            adj_matrix[i, i + 1] = 1

    return adj_matrix


def create_two_path_matrix(top_edges, bottom_edges, randomize=False):
    if top_edges < 2 or bottom_edges < 2:
        raise ValueError("Number of edges must be at least 2")

    # Calculate total number of nodes
    total_nodes = top_edges + bottom_edges

    # Initialize an empty adjacency matrix
    adj_matrix = np.zeros((total_nodes, total_nodes), dtype=int)

    # Create top path
    for i in range(top_edges - 1):
        if randomize:
            adj_matrix[i, i + 1] = random.randint(1, 10)
        else:
            adj_matrix[i, i + 1] = 1

    # Create bottom path
    adj_matrix[0, top_edges] = 1
    for i in range(bottom_edges - 1):
        adj_matrix[top_edges + i, top_edges + i + 1] = 1

    # Connect the last node of the top path to the last node of the bottom path
    adj_matrix[top_edges - 1, top_edges + bottom_edges - 1] = 1

    return adj_matrix


if __name__ == "__main__":
    a_matrix = [[0, 1, 0], [0, 0, 2], [0, 0, 0]]
    b_matrix = [[0, 2, 0], [0, 0, 1], [0, 0, 0]]
    c_matrix = [[0, 1, 0], [0, 0, 1], [0, 0, 0]]

    # Save the matrices to CSV files
    save_matrix_to_csv(a_matrix, './../data/network1/a_matrix.csv')
    save_matrix_to_csv(b_matrix, './../data/network1/b_matrix.csv')
    save_matrix_to_csv(c_matrix, './../data/network1/c_matrix.csv')
