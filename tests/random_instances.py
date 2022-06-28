import pickle
import random
from math import ceil

from tqdm import tqdm

from src.election_instance import *
from src.helpers import check_optimality
from src.rules.interval_knapsack import interval_knapsack_projects


def random_project(min_cost, max_cost):
    start = random.random()
    size = random.uniform(0, 1 - start)
    if min_cost == max_cost:
        cost = min_cost
    else:
        cost = random.randint(min_cost, max_cost)
    return Project(start, size, cost)


def random_approvals(voters, projects):
    approvals = {}
    for v in voters:
        num = random.randint(1, len(projects))
        approvals[v] = random.sample(projects, num)
    return approvals


def random_instance(N, p):
    voters = [i for i in range(1, N + 1)]
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
    ik_result = interval_knapsack_projects(E)

    if not check_optimality(E, ik_result):
        pickle.dump(E, open("bad_instance" + str(id) + ".p", "wb"))
        raise ValueError("interval knapsack failed on:" + str())


def random_checks(k, min_N=50, max_N=1000, min_p=5, max_p=15):
    for i in tqdm(range(k)):
        N = random.randint(min_N, max_N)
        p = random.randint(min_p, max_p)
        random_check(i, N, p)


def main():
    random_checks(100000, 100, 1000000, 5, 30)


if __name__ == "__main__":
    main()
