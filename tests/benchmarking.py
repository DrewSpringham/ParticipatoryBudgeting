import pickle
import timeit

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

from src.rules.interval_knapsack import interval_knapsack_projects


def generate():
    count = 0
    (xs, times, old_es) = pickle.load(open("C:/Users/Student/Documents/GitHub/PB/tests/data_reversed.pickle", "rb"))
    times = []
    xs = []
    es = []
    try:
        for E in old_es:

            count += 1
            start = timeit.default_timer()

            ik_result = interval_knapsack_projects(E)
            end = timeit.default_timer()
            time = end - start
            times.append(time)
            es.append(E)
            xs.append(len(E.projects) * len(E.projects) * E.budget)
            if count % 10 == 0:
                x = np.array(xs)
                y = np.array(times)
                gradient, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                mn = np.min(x)
                mx = np.max(x)
                x1 = np.linspace(mn, mx, 500)
                y1 = gradient * x1 + intercept
                plt.plot(x, y, 'xb')
                plt.plot(x1, y1, '-r')

                plt.xlabel(f"Number of projects squared times number of voters.")
                plt.ylabel("Time (s)")
                plt.title(
                    "Number of projects squared times number of voters runtime\nof optimised knapsack algorithm.")
                plt.show()

    except KeyboardInterrupt:
        with open('data.pickle', 'wb') as handle:
            pickle.dump((xs, times, es), handle, protocol=pickle.HIGHEST_PROTOCOL)
        x = np.array(xs)
        y = np.array(times)
        gradient, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        mn = np.min(x)
        mx = np.max(x)
        x1 = np.linspace(mn, mx, 500)
        y1 = gradient * x1 + intercept
        plt.plot(x, y, 'ob')
        plt.plot(x1, y1, '-r')

        plt.xlabel(f"Number of projects squares times number of voters.\nr-value of {r_value}")
        plt.ylabel("Time (s)")
        plt.title(
            "Number of projects squares times number of voters runtime\nof knapsack algorithm.")
        plt.show()


def load():
    (xs, times, es) = pickle.load(open("data_reversed.pickle", "rb"))

    x = np.array(xs)
    y = np.array(times)
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    mn = np.min(x)
    mx = np.max(x)
    x1 = np.linspace(mn, mx, 500)
    y1 = gradient * x1 + intercept
    plt.plot(x, y, 'ob')
    plt.plot(x1, y1, '-r')

    plt.xlabel(f"Number of projects squares times number of voters.\nr-value of {r_value}")
    plt.ylabel("Time (s)")
    plt.title(
        "Number of projects squares times number of voters runtime\nof knapsack algorithm.")
    plt.show()


if __name__ == "__main__":
    generate()
