import pickle
from math import ceil

from tqdm import tqdm

from src.election_instance import *
from src.helpers import check_optimality
from src.rules.interval_knapsack import interval_knapsack_projects


def random_project_midpoint(min_cost, max_cost):
    mid = random.random()
    dist_to_edge = min(1 - mid, mid)
    radius = random.uniform(0, dist_to_edge)
    start = mid - radius
    size = 2 * radius
    if min_cost == max_cost:
        cost = min_cost
    else:
        cost = random.randint(min_cost, max_cost)
    return Project(start, size, cost)


def random_project_start_then_size(min_cost, max_cost):
    start = random.random()
    size = random.uniform(0, 1 - start)
    if min_cost == max_cost:
        cost = min_cost
    else:
        cost = random.randint(min_cost, max_cost)
    return Project(start, size, cost)


def random_project_size_then_start(min_cost, max_cost):
    size = random.random()
    start = random.uniform(0, 1 - size)

    if min_cost == max_cost:
        cost = min_cost
    else:
        cost = random.randint(min_cost, max_cost)
    return Project(start, size, cost)


def random_project(min_cost, max_cost):
    return random_project_size_then_start(min_cost, max_cost)


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
        projects.append(random_project(5000, 100000))
    approvals = random_approvals(voters, projects)
    average_cost = sum([P.cost for P in projects]) / p
    budget = ceil(average_cost * random.randint(1, p) * random.random())
    E = Election(voters, projects, approvals, None, budget)
    return E


def random_check(id, N, p, rule):
    E = random_instance(N, p)
    ik_result = rule(E)

    if not check_optimality(E, ik_result):
        pickle.dump(E, open("bad_instance" + str(id) + ".p", "wb"))
        raise ValueError("interval knapsack failed on:" + str())


def random_checks(k, rule, min_N=50, max_N=1000, min_p=5, max_p=15):
    for i in tqdm(range(k)):
        N = random.randint(min_N, max_N)
        p = random.randint(min_p, max_p)
        random_check(i, N, p, rule)


def random_instances(k, min_N, max_N, min_p, max_p):
    for i in range(k):
        N = random.randint(min_N, max_N)
        p = random.randint(min_p, max_p)
        yield random_instance(N, p)


def main():
    random_checks(1000, interval_knapsack_projects)


if __name__ == "__main__":
    main()
