import networkx as nx

# Function to create a graph with latency functions using the modified matrices
def create_graph_with_latency_modified(n, a_matrix, b_matrix, c_matrix):
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if a_matrix[i][j] != 0 or b_matrix[i][j] != 0 or c_matrix[i][j] != 0:  # Check if an edge exists
                G.add_edge(i, j, a=a_matrix[i][j], b=b_matrix[i][j], c=c_matrix[i][j])
    return G