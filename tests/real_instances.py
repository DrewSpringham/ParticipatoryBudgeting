import os

from tqdm import tqdm

from src.helpers import check_optimality
from src.rules.reverse_interval_knapsack import interval_knapsack_projects_reversed
from tests.pabulib_converter import convert_to_election


def real_instances(up_to=None):
    """
    Generator for real instances
    :param up_to: An optional limiter to limit the number of instances to return
    """
    directory = "../tests/pb_files_loc/"
    files = os.listdir(directory)
    if up_to is not None:
        files = files[:up_to]
    for filename in tqdm(files):
        f = os.path.join(directory, filename)
        print(f)
        # checking if it is a file
        if os.path.isfile(f):
            E = convert_to_election(f)
            yield E


def real_checks(rule):
    for E in real_instances():
        ik_result = rule(E)
        if not check_optimality(E, ik_result):
            raise ValueError(f"Real checks failed, check file {E.election_id}")


def main():
    real_checks(interval_knapsack_projects_reversed)
