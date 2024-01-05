import networkx as nx
X = 10
# Function to create a graph with latency functions using the modified matrices
def find_shortest_path(G: nx.DiGraph(), source, target):
    G2 = solve_graph(G)
    nx.shortest_path(G, source=source, target=target, weight='weight')

def solve_graph(G: nx.DiGraph()):
    G2 = nx.DiGraph()
    
    for edge in G.edges(data=True):
        src, dst, abc = edge
        a = abc['a']
        b = abc['b']
        c = abc['c']
        y = a*X*X + b*X + c
        G2.add_edge(src, dst, weight=y)
    return G2
