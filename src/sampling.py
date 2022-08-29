import random
import string
import timeit
from math import ceil, log

import pandas as pd
from tqdm import trange

from src.election_instance import Election
from src.rules.basic_single_ejr import basicejr
from tests.pabulib_converter import convert_to_election
from tests.random_instances import random_instances
from tests.real_instances import real_instances


# TODO: document
def is_single(E):
    """
    Check if an election is a single approval election
    :param E: An election
    :return: If the election is a single approval election
    """
    single = True
    # Check that every voter only votes for a single candidate
    for v in E.voters:
        if len(E.approvals[v]) != 1:
            single = False
    return single


def check_EJR_single_approval(E, W):
    """
    For an single approval election, compute the true EJR error of the project set W
    :param E: An election
    :param W: A winning set of projects
    :return true_eps: true_eps which is the max value of eps over each project p such that p is not in W and the number
    of voters of p is (1+eps)(cost(p)*n/b)
    """
    true_eps = 0
    for p in E.projects:
        G_size = E.approvals_by_project[p]
        req_size = p.cost * len(E.voters) / E.budget
        if G_size >= req_size and p not in W:
            true_eps = max(true_eps, G_size / req_size - 1)
    return true_eps


def create_subelection(E, s):
    """
    Create a new election derived from E with a sample of the voters of size s
    :param E: An election
    :param s: A sample size of the voters
    :return: A new election derived from E
    """
    S = set(random.sample(list(E.voters), s))
    subapprovals = E.approvals.copy()
    # Remove all voters not in the sample S
    for v in E.voters:
        if v not in S:
            del subapprovals[v]
    subelection = Election(S, E.projects, subapprovals, None, E.budget)
    return subelection


def test_election(E, source_name, runs, max_eps, eps_step_per_unit, delta):
    elections = {'election_id': [], 'voters': [], 'projects': [], 'budget': [], 'min_cost': []}
    results = {'election_id': [], 'rule_id': [], 'run_id': [], 'delta': [], 'eps': [], 'real_eps': []}
    # wrap in try so we can save current results at any timr
    try:
        # only works if election is single
        if is_single(E):
            min_cost = min([p.cost for p in E.projects]) + 0.0001
            elections['election_id'].append(E.election_id)
            elections['voters'].append(len(E.voters))
            elections['projects'].append(len(E.projects))
            elections['budget'].append(E.budget)
            elections['min_cost'].append(min_cost)

            m = len(E.projects)
            for eps_i in range(max_eps * eps_step_per_unit):
                # eps_i runs from 0 to max_eps* number of steps per unit of epsilon, so to get a value of eps we transform
                eps = (eps_i + 1) / eps_step_per_unit
                # get sample size from bound
                s = ceil(E.budget ** 2 * log(m / delta) / (2 * eps ** 2 * min_cost ** 2))
                # only try to sample if sample size is less than whole population
                if s <= len(E.voters):
                    print(f"EPSILON: {eps}\n")
                    print(f"SAMPLE SIZE {s}")
                    # run this configuration runs number of times
                    for _ in trange(runs):
                        subelection = create_subelection(E, s)
                        W = basicejr(subelection)
                        real_eps = check_EJR_single_approval(E, W)
                        results['election_id'].append(E.election_id)
                        results['rule_id'].append("BasicJR")
                        # choose random id for the run to easily select a specific run in analysis
                        r_id = ''.join(random.choice(string.ascii_letters) for _ in range(64))
                        results['run_id'].append(r_id)
                        results['delta'].append(delta)
                        results['eps'].append(eps)
                        results['real_eps'].append(real_eps)
    finally:
        # save the results once we finish or error (or keyboard interupt)
        try:
            election_frame = pd.DataFrame(elections)
            res_frame = pd.DataFrame(results)
            election_frame.to_csv(f'elections_{source_name}.csv', mode='a', index=False, header=False)
            res_frame.to_csv(f'results_{source_name}.csv', mode='a', index=False, header=False)
        except PermissionError:
            t = timeit.default_timer()

            election_frame = pd.DataFrame(elections)
            res_frame = pd.DataFrame(results)
            election_frame.to_csv(f'elections_{ceil(t)}.csv', index=False, header=False)
            res_frame.to_csv(f'results_{ceil(t)}.csv', index=False, header=False)


def main(source_name, runs, max_eps, eps_step_per_unit, delta):
    f = "../tests/pb_files/poland_wroclaw_2015_from-500.pb"
    if source_name == "real":
        source = real_instances()
    elif source_name == "only":
        source = [convert_to_election(f)]
    elif source_name == "random":
        source = random_instances(50, 1000, 300000, 3, 70)
    else:
        raise ValueError("Source name not defined")
    for E in source:
        test_election(E, source_name, runs, max_eps, eps_step_per_unit, delta)


if __name__ == "__main__":
    main(source_name="random", runs=500, max_eps=5, eps_step_per_unit=20, delta=0.05)
