import networkx as nx


def create_graph_from_matrices(a_matrix, b_matrix, c_matrix):
    n = len(a_matrix)
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            # Check if an edge exists
            if a_matrix[i][j] != 0 or b_matrix[i][j] != 0 or c_matrix[i][j] != 0:
                G.add_edge(i, j, a=a_matrix[i][j], b=b_matrix[i][j], c=c_matrix[i][j])
    return G
