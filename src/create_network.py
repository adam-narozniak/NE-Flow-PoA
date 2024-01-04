import csv


def save_matrix_to_csv(matrix, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in matrix:
            # Replace 'None' with an empty string for CSV
            cleaned_row = ["" if element is None else element for element in row]
            writer.writerow(cleaned_row)


if __name__ == "__main__":
    a_matrix = [[0, 1, 0], [0, 0, 2], [0, 0, 0]]
    b_matrix = [[0, 2, 0], [0, 0, 1], [0, 0, 0]]
    c_matrix = [[0, 1, 0], [0, 0, 1], [0, 0, 0]]

    # Save the matrices to CSV files
    save_matrix_to_csv(a_matrix, './../data/network1/a_matrix.csv')
    save_matrix_to_csv(b_matrix, './../data/network1/b_matrix.csv')
    save_matrix_to_csv(c_matrix, './../data/network1/c_matrix.csv')


