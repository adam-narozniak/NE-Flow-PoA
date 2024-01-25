import NE_continous as ne
from social_optimum import find_social_optimum


def calculate_price_of_anarchy(G):
    """Given graph calculate the price of anarchy."""

    flow_fractions, total_latency = find_social_optimum(G)
    social_optimum = total_latency

    G, partition, paths, final_latencies = ne.calculate_nash_flow(G, 0, len(G) - 1)
    nash_equlibrium_value = final_latencies[0]

    return nash_equlibrium_value / social_optimum


if __name__ == "__main__":
    from loading_utils import create_graph
    directory = f"../data/network1/"
    G = create_graph(directory)
    calculate_price_of_anarchy(G)
    print(calculate_price_of_anarchy(G))