import os

from tqdm import tqdm

from src.helpers import check_optimality
from src.rules.interval_knapsack import interval_knapsack_projects
from tests.pabulib_converter import convert_to_election


def real_instances(rule):
    directory = "pb_files_loc"
    for filename in tqdm(os.listdir(directory)):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):

            E = convert_to_election(f)
            ik_result = rule(E)

            if not check_optimality(E, ik_result):
                raise ValueError(f"interval knapsack failed on: {f}")


if __name__ == "__main__":
    real_instances(interval_knapsack_projects)
