import pickle
import random
from math import ceil

from more_itertools import powerset
from tqdm import tqdm

from src.election_instance import *
from src.helpers import verify_outcome
from src.rules.interval_knapsack import interval_knapsack_score


def random_project(min_cost, max_cost):
    start = random.random()
    size = random.uniform(0, 1 - start)
    cost = random.randint(min_cost, max_cost)
    return Project(start, size, cost)


def random_approvals(voters, projects):
    approvals = {}
    for v in voters:
        num = random.randint(1, len(projects))
        approvals[v] = random.sample(projects, num)
    return approvals


def random_instance(N, p):
    voters = [i for i in range(1, N)]
    projects = []
    for i in range(p):
        projects.append(random_project(1, p))
    approvals = random_approvals(voters, projects)
    average_cost = sum([p.cost for p in projects]) / p
    budget = ceil(average_cost * random.randint(1, p))
    E = Election(voters, projects, approvals, budget)
    return E


def random_check(id, N, p):
    E = random_instance(10, 10)
    max_approvals = 0
    max_project_set = None
    for s in powerset(E.projects):
        if verify_outcome(E, s):
            total_approvals = sum([E.approvals_by_project[v] for v in s])
            if total_approvals > max_approvals:
                max_approvals = total_approvals
                max_project_set = s
    ik_result = interval_knapsack_score(E)
    if ik_result != max_approvals:
        pickle.dump(E, open("bad_instance" + str(id) + ".p", "wb"))
        raise ValueError("interval knapsack failed on:" + str())


def random_checks(k):
    for i in tqdm(range(k)):
        N = random.randint(50, 1000)
        p = random.randint(5, 15)
        random_check(i, N, p)


def main():
    random_checks(100000)


if __name__ == "__main__":
    main()
