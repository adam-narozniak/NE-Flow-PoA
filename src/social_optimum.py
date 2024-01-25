from scipy.optimize import minimize
import numpy as np

def Latency(x, paths, p_s):
        """
        Finds the latency of the graph given the flow
        x - flow in a graph
        """
        L = 0
        for i_path, path in enumerate(paths):
            L_path = 0
            for edge in path:
                a = edge[2]['a']
                b = edge[2]['b']
                c = edge[2]['c']

                p_edge = p_s[(edge[0], edge[1])]
                x_edge = 0
                x_edge_string = ''
                for i in p_edge:
                    x_edge += x[i]

                    x_edge_string += f' x{i-1}+'
                L_path += a * (x_edge)**2 + b * x_edge + c
            L += x[i_path] * L_path
        return L

def social_optimum(paths, p_s):
    """
    Finds the socially optimal flow of in a graph 
    G_modified - graph with latency functions
    """
    # paths = ne.find_all_paths(G_modified, 0, len(G_modified.nodes)-1)
    # p_s = ne.create_latency_fun(paths)

    n  = len(paths)
    # f - flow
    f = np.array([0] * n)

    def Latency(x):
        """
        Finds the latency of the graph given the flow
        x - flow in a graph
        """
        L = 0
        for i_path, path in enumerate(paths):
            L_path = 0
            for edge in path:
                a = edge[2]['a']
                b = edge[2]['b']
                c = edge[2]['c']

                p_edge = p_s[(edge[0], edge[1])]
                x_edge = 0
                for i in p_edge:
                    x_edge += x[i]
                L_path += a * (x_edge)**2 + b * x_edge + c
            L += x[i_path] * L_path
        return L
        
    start_flow = np.array([1/n]*n)
    bounds = [(0,1)] * n
    cons = ({'type': 'eq', 'fun': lambda x:  sum(x)-1})
    minimum = minimize(Latency, start_flow, bounds=bounds, constraints=cons)
    return minimum.x, minimum.fun 