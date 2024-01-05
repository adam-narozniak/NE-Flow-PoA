import csv


def load_matrix_from_csv(filename):
    matrix = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert back empty strings to 'None'
            cleaned_row = [None if element == "" else float(element) for element in row]
            matrix.append(cleaned_row)
    return matrix