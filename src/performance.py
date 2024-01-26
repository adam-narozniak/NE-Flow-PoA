import timeit

import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

from social_optimum import find_social_optimum
from NE_continous import calculate_nash_flow
from nash_equilibrium import find_nash_equilibrium_from_graph


def gather_performance_data(graphs_list, algorithm="so"):
    results = {}
    raw_times = {}
    for i, G in enumerate(graphs_list):
        print(f"Graph {i}")
        if algorithm == "so":
            fnc = find_social_optimum
        elif algorithm == "ne-analytical":
            fnc = find_nash_equilibrium_from_graph
        elif algorithm == "ne":
            fnc = calculate_nash_flow
        else:
            raise ValueError("The given algorithm is not available.")
        time_taken_np = np.array(
            timeit.repeat(lambda: fnc(G.copy()), globals=globals(),
                          number=100, repeat=1))
        mean = np.mean(time_taken_np)
        results[i + 1] = {"nodes": len(G.nodes()), "edges": len(G.edges()),
                          "mean": mean, "std": np.std(time_taken_np)}
        raw_times[i + 1] = time_taken_np
        print(results[i + 1])
    return results, raw_times


def gather_performance_data_all(graphs_list):
    all_results = {}
    all_raw_times = {}
    for algorithm in ["so", "ne-analytical", "ne"]:
        print(f"Algorithm: {algorithm}")
        results, raw_times = gather_performance_data(graphs_list, algorithm)
        all_results[algorithm] = results
        all_raw_times[algorithm] = raw_times
    return all_results, all_raw_times


def linear_model(x, a, b):
    return a * x + b


def quadratic_model(x, a, b, c):
    return a * x ** 2 + b * x + c


def cubic_model(x, a, b, c, d):
    return a * x ** 3 + b * x ** 2 + c * x + d


def logarithmic_model(x, a, b):
    return a * np.log(x) + b


def fit_models_and_calculate_r2(results):
    all_r2_scores = {}
    all_predicted_y = {}
    for algo, values in results.items():
        num_edges = [value["edges"] for value in values.values()]
        times = [value["mean"] for value in values.values()]

        models = {
            'Linear': linear_model,
            'Quadratic': quadratic_model,
            'Logarithmic': logarithmic_model,
        }
        r2_scores = {}
        predicted_ys = {}

        for name, model in models.items():
            params, _ = curve_fit(model, num_edges, times, maxfev=10000)
            predicted_y = model(np.array(num_edges), *params)
            r2_scores[name] = r2_score(times, predicted_y)
            predicted_ys[name] = predicted_y

        all_r2_scores[algo] = r2_scores
        all_predicted_y[algo] = predicted_ys
    return all_r2_scores, all_predicted_y
