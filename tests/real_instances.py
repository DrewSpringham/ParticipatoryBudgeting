import os

from tqdm import tqdm

from src.rules.interval_knapsack import interval_knapsack_projects, interval_knapsack_projects_reversed
from tests.pabulib_converter import convert_to_election


def real_instances(rule, up_to=None):
    directory = "pb_files_loc"
    count = 0
    files = os.listdir(directory)
    if up_to is not None:
        files = files[:up_to]
    for filename in tqdm(files):
        f = os.path.join(directory, filename)

        # checking if it is a file
        if os.path.isfile(f):
            E = convert_to_election(f)
            ik_result = rule(E)
            count += 1

            # if not check_optimality(E, ik_result):
            # raise ValueError(f"interval knapsack failed on: {f}")


if __name__ == "__main__":
    real_instances(interval_knapsack_projects_reversed)
    real_instances(interval_knapsack_projects)
