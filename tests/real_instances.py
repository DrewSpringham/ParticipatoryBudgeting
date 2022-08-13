import os
import timeit
from math import log

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from tqdm import tqdm

from src.rules.reverse_interval_knapsack import interval_knapsack_projects_reversed
from tests.pabulib_converter import convert_to_election


def real_instances(up_to=None):
    directory = "../tests/pb_files_loc/"
    count = 0
    files = os.listdir(directory)
    if up_to is not None:
        files = files[:up_to]
    for filename in tqdm(files):
        f = os.path.join(directory, filename)
        print(f)
        # checking if it is a file
        if os.path.isfile(f):
            E = convert_to_election(f, count)
            yield E
            count += 1

            # if not check_optimality(E, ik_result):
            # raise ValueError(f"interval knapsack failed on: {f}")


if __name__ == "__main__":
    times1 = []
    times2 = []
    xs = {'voters': [], 'projects': [], 'logvoters': [], 'logprojects': [], 'budget': [], 'voterproj^2': []}
    count = 0
    for E in real_instances():
        count += 1
        start = timeit.default_timer()

        ik_result = interval_knapsack_projects_reversed(E)
        end = timeit.default_timer()
        time1 = end - start
        """
        start = timeit.default_timer()

        ik_result = interval_knapsack_projects(E)
        end = timeit.default_timer()
        time2 = end - start
        """
        times1.append(time1)
        # times2.append(time2)
        xs['voters'].append(len(E.voters))
        xs['logvoters'].append(log(len(E.voters)))
        xs['projects'].append(len(E.projects))
        xs['logprojects'].append(log(len(E.projects)))
        xs['budget'].append(E.budget)
        xs['voterproj^2'].append(len(E.voters) * len(E.projects) ** 2)
    x = np.array(xs['projects'])
    y_rev = np.array(times1)
    # y = np.array(times2)

    gradient, intercept, r_value, p_value, std_err = stats.linregress(x, y_rev)
    print(gradient, intercept, r_value, p_value, std_err)

    mn = np.min(x)
    mx = np.max(x)
    x1 = np.linspace(mn, mx, 500)
    y1 = gradient * x1 + intercept
    plt.plot(x, y_rev, 'xb')
    plt.plot(x1, y1, '-r')
    """
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print(gradient, intercept, r_value, p_value, std_err)
    y2 = gradient * x1 + intercept
    plt.plot(x, y, 'xg')
    plt.plot(x1, y2, '-y')
    """
    plt.xlabel("Number of projects squared times number of voters ")
    plt.ylabel("Time (s)")
    plt.title(
        "Number of projects squared times number of voters\n against runtime of optimised knapsack algorithm")

    plt.show()
