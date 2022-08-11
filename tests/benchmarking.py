import timeit

import pandas as pd
from openpyxl import load_workbook

from src.rules.interval_knapsack import interval_knapsack_projects
from src.rules.reverse_interval_knapsack import interval_knapsack_projects_reversed
from tests.random_instances import random_instances
from tests.real_instances import real_instances


def generate(data_source, rules):
    elections = {'election_id': [], 'voters': [], 'projects': [], 'budget': []}
    times = {'election_id': [], 'rule_id': [], 'time': []}
    if data_source == 'random':
        source = random_instances(10000, 100, 100000, 5, 50)
    elif data_source == 'real':
        source = real_instances()
    else:
        raise ValueError("Unknown data source!")
    try:
        stop = False
        print("Starting testing")
        for E in source:
            election_id = E.election_id
            print(f"Testing election {election_id}")
            elections['election_id'].append(election_id)
            elections['voters'].append(len(E.voters))
            elections['projects'].append(len(E.projects))
            elections['budget'].append(E.budget)
            for (rule, rule_id) in rules:
                start = timeit.default_timer()
                ik_result = rule(E)
                end = timeit.default_timer()
                time = end - start
                print(f"Finished on rule {rule_id}")
                times['election_id'].append(election_id)
                times['rule_id'].append(rule_id)
                times['time'].append(time)
                """
                if time>180:
                    stop=True
                    break
                """
            if stop:
                break
        raise KeyboardInterrupt
    except KeyboardInterrupt:
        path = f"benchmarks_{data_source}.xlsx"
        with pd.ExcelWriter(path, mode="a", if_sheet_exists='overlay', engine="openpyxl") as writer:

            election_frame = pd.DataFrame(elections)
            times_frame = pd.DataFrame(times)
            book = load_workbook(path)
            writer.book = book
            writer.sheets = {ws.title: ws for ws in book.worksheets}
            election_frame.to_excel(writer, startrow=writer.sheets['Elections'].max_row, header=False, index=False,
                                    sheet_name="Elections")
            times_frame.to_excel(writer, startrow=writer.sheets['Times'].max_row, header=False, index=False,
                                 sheet_name="Times")


if __name__ == "__main__":
    generate('real', [
        (interval_knapsack_projects_reversed, 2),
        (interval_knapsack_projects, 1)  # ,
        # (naive_interval_knapsack_projects, 0)
    ])
