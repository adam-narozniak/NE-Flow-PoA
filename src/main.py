import argparse

import nash_equilibrium as ne
import social_optimum as so
from loading_utils import load_matrix_from_csv
from network import create_graph_from_matrices
from NE_continous import calculate_nash_flow
from src.visualize_flow import visualize_flow
from visualize import visualize_network
import pathlib


def create_parser():
    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument(
        "--directory-path",
        type=str,
        default="../data/network5/",
        required=False,
        help="Path to the directory with coefficient_matrices.",
    )
    parser.add_argument(
        "--save-path",
        type=str,
        default="../images/network5/",
        help="Path to the directory where the images of network will be saved.",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        choices=["so", "ne", "ne-analytical", "ne-discrete", "poa"],
        default="poa",
        help="Type of algorithm to run.",
    )
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        help="Print all the path etc.",
    )
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    path = args.directory_path
    image_save_directory_path = args.save_path
    if not pathlib.Path(image_save_directory_path).exists():
        pathlib.Path(image_save_directory_path).mkdir(parents=True)
    verbose = args.verbose
    algorithm = args.algorithm

    # Load the matrices back from the CSV files
    loaded_a_matrix = load_matrix_from_csv(path + 'a_matrix.csv')
    loaded_b_matrix = load_matrix_from_csv(path + 'b_matrix.csv')
    loaded_c_matrix = load_matrix_from_csv(path + 'c_matrix.csv')
    G = create_graph_from_matrices(loaded_a_matrix, loaded_b_matrix,
                                   loaded_c_matrix)
    visualize_network(G, image_save_directory_path + "network.jpg")

    A = 0
    B = len(G) - 1
    paths = ne.find_all_paths(G, A, B)

    if verbose:
        print(G.edges(data=True))  # Display the edges with latency function attributes
        print(f"All paths from {A} to {B} are presented below:")
        for i, path in enumerate(paths):
            print(f"path {i + 1} - {path}")
        print()

    p_s = ne.create_latency_fun(paths)
    if algorithm == "ne-analytical":
        # for key in p_s:
        #     print(f"Edge {key} is contained in following paths: {p_s[key]}")
        # print('----------------')
        print('Nash Equilibrium:')
        ne_res = ne.find_nash_equilibrium(paths, p_s)
        flows, latency = ne_res
        print(ne_res)
    elif algorithm == "so":
        print('----------------')
        print('Social Optimum:')
        sopt = so.social_optimum(paths, p_s)
        flows, latency = sopt
        visualize_flow(G, p_s, flow=flows,
                       savepath=image_save_directory_path + "flow_so.jpg")
        print(sopt)

    elif algorithm == "ne":
        print('Nash Equilibrium:')
        ne_res = calculate_nash_flow(G)
        flows, latency = ne_res[1], ne_res[3][0]
        visualize_flow(G, p_s, flow=flows,
                       savepath=image_save_directory_path + "flow_ne.jpg")
        print((flows, latency))
    elif algorithm == "poa":
        print('Price of Anarchy:')
        print('Nash Equilibrium:')
        ne_res = calculate_nash_flow(G)
        flows, latency = ne_res[1], ne_res[3][0]
        visualize_flow(G, p_s, flow=flows,
                       savepath=image_save_directory_path + "flow_ne.jpg")
        print(flows, latency)
        print('Social Optimum:')
        sopt = so.social_optimum(paths, p_s)
        flows, latency = sopt
        visualize_flow(G, p_s, flow=flows,
                       savepath=image_save_directory_path + "flow_so.jpg")
        print(sopt)
        print(f"POA: {ne_res[3][0] / sopt[1]}")
    else:
        print("Incorrect algorithm name.")
