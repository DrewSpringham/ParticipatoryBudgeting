import pickle
from math import ceil

from tqdm import tqdm

from src.election_instance import *
from src.helpers import check_optimality
from src.rules.standard_interval_knapsack import interval_knapsack_projects


def random_project_midpoint(min_cost, max_cost):
    """
    Create a random project by selecting a random midpoint and then size
    :param min_cost: A minimum cost of the project
    :param max_cost: A maximum cost of the project
    :return: A random project with the parameters given
    """
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
    """
        Create a random project by selecting a random start point and then size
        :param min_cost: A minimum cost of the project
        :param max_cost: A maximum cost of the project
        :return: A random project with the parameters given
        """
    start = random.random()
    size = random.uniform(0, 1 - start)
    if min_cost == max_cost:
        cost = min_cost
    else:
        cost = random.randint(min_cost, max_cost)
    return Project(start, size, cost)


def random_project_size_then_start(min_cost, max_cost):
    """
        Create a random project by selecting a random size and then start point
        :param min_cost: A minimum cost of the project
        :param max_cost: A maximum cost of the project
        :return: A random project with the parameters given
        """
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
    """
    Generate a random approval dict given the voters and projects
    :param voters: Set of voters
    :param projects: Set of projects
    :return: Random approval function
    """
    approvals = {}
    for v in voters:
        num = random.randint(1, len(projects))
        approvals[v] = random.sample(projects, num)
    return approvals


def random_instance(N, p):
    """
    Generates a random election with at N voters and p projects
    :param N: Number of voters for the election
    :param p: Number of projects for the election
    :return: An election with those parameters
    """
    voters = [i for i in range(1, N + 1)]
    projects = []
    for i in range(p):
        # generate p random projects
        projects.append(random_project(5000, 100000))
    approvals = random_approvals(voters, projects)
    # find average cost of project
    average_cost = sum([P.cost for P in projects]) / p
    # select the budget randomly to be between the average cost of a single project and the sum of all the costs
    budget = ceil(average_cost * random.uniform(1, p))
    E = Election(voters, projects, approvals, None, budget)
    return E


def random_instances(k, min_N, max_N, min_p, max_p):
    """
    Generate k random election
    :param k: The number of elections to generate
    :param min_N: The minimum number of voters in each election
    :param max_N: The max. number of voters in each election
    :param min_p: The min. number of projects in each election
    :param max_p: the max. number of porjects in each election
    """
    for i in range(k):
        N = random.randint(min_N, max_N)
        p = random.randint(min_p, max_p)
        yield random_instance(N, p)


def random_check(N, p, rule):
    """
    Verify that the elction rule is correct on a random instance
    :param N: The number of voters in the random instance
    :param p: The number of project in the random instance
    :param rule: The rule to test
    """
    E = random_instance(N, p)
    ik_result = rule(E)

    if not check_optimality(E, ik_result):
        pickle.dump(E, open("bad_instance.p", "wb"))
        raise ValueError("Random checks failed, check pickle file.")


def random_checks(k, rule, min_N=50, max_N=1000, min_p=5, max_p=15):
    """
    Test an election rule k times for correctness against random instances
    :param k: The number of tests to run
    :param rule: The election rule
    :param min_N: The min number of voters in the test
    :param max_N: the max number of voters in the test
    :param min_p: The min number of projects in the test
    :param max_p: The max number of porjects in the test
    """
    for _ in tqdm(range(k)):
        N = random.randint(min_N, max_N)
        p = random.randint(min_p, max_p)
        random_check(N, p, rule)


def main():
    random_checks(1000, interval_knapsack_projects)


if __name__ == "__main__":
    main()
