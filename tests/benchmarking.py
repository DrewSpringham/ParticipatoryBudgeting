import timeit
from math import ceil

import pandas as pd

from src.rules.reverse_interval_knapsack import interval_knapsack_projects_reversed
from src.rules.standard_interval_knapsack import interval_knapsack_projects
from tests.random_instances import random_instances
from tests.real_instances import real_instances


def generate(data_source, rules):
    """
    Benchmarks the time election rules take for different elections, and saves the data
    :param data_source: A string of which data source to use. Either "random" or "real"
    :param rules: a list of tuples of rules and rule ids
    """
    elections = {'election_id': [], 'voters': [], 'projects': [], 'budget': []}
    times = {'election_id': [], 'rule_id': [], 'time': []}
    if data_source == 'random':
        source = random_instances(10, 1000, 300000, 3, 70)
    elif data_source == 'real':
        source = real_instances()
    else:
        raise ValueError("Unknown data source!")
    try:
        print("Starting testing")
        for n, E in enumerate(source):

            election_id = E.election_id
            print(f"Testing election {n}")
            elections['election_id'].append(election_id)
            elections['voters'].append(len(E.voters))
            elections['projects'].append(len(E.projects))
            elections['budget'].append(E.budget)
            for (rule, rule_id) in rules:
                # We time how long it takes for a rules to compute a winning set
                start = timeit.default_timer()
                ik_result = rule(E)
                end = timeit.default_timer()
                time = end - start
                print(f"Finished on rule {rule_id}")
                times['election_id'].append(election_id)
                times['rule_id'].append(rule_id)
                times['time'].append(time)
    finally:
        try:
            # We save the data to a csv file for external analysis
            election_frame = pd.DataFrame(elections)
            res_frame = pd.DataFrame(times)
            election_frame.to_csv(f'bench_elections_{data_source}.csv', mode='a', index=False, header=False)
            res_frame.to_csv(f'bench_results_{data_source}.csv', mode='a', index=False, header=False)
        except PermissionError:
            t = timeit.default_timer()

            election_frame = pd.DataFrame(elections)
            res_frame = pd.DataFrame(times)
            election_frame.to_csv(f'bench_elections_{ceil(t)}.csv', index=False, header=False)
            res_frame.to_csv(f'bench_results_{ceil(t)}.csv', index=False, header=False)
        finally:
            print("Saved")


if __name__ == "__main__":
    while True:
        generate('random', [
            (interval_knapsack_projects_reversed, 2),
            (interval_knapsack_projects, 1)
        ])
