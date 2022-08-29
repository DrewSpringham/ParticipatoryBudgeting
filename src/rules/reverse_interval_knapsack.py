import math

from src.election_instance import Election
from src.helpers import compute_preceding_projects


def interval_knapsack_table_reversed(E: Election):
    """
    Creates the reverse knapsack dynamic programming table
    :param E: An election
    :return T,upper: the dynamic programming table T, and upper which is the max utility achievable with budget b
    """
    m = len(E.projects)
    max_total_approvals = sum([E.approvals_by_project[p] for p in E.projects])
    # Projects sorted by end point
    P = list(sorted(E.projects, key=lambda p: p.end))
    b = E.budget
    # set up table
    T = [[None for _ in range(1 + max_total_approvals)] for _ in range(m + 1)]
    # Compute a dict index by projects p of the last project that lies wholly before p on the interval
    prec_projects = compute_preceding_projects(P)
    # need infinite weight limit to achieve any utility with no items
    for u in range(1 + max_total_approvals):
        T[0][u] = math.inf
    # can achieve o utility with any number of projects
    for i in range(m + 1):
        T[i][0] = 0
    lower_bound = 0
    upper_bound = max_total_approvals
    # binary search style loop
    while lower_bound < upper_bound:
        r = (lower_bound + upper_bound + 1) // 2
        to_compute = [(m, r)]
        # Computing table elements on demand, so we can get the value of T[m][r]
        while len(to_compute) > 0:
            i, u = to_compute.pop()
            # Value of item i
            vi = E.approvals_by_project[P[i - 1]]
            # weight of item i
            wi = P[i - 1].cost
            # the index of the project that lies wholly to the left of project i (-1 if it doesn't exist)
            t = prec_projects[i]
            # if we include project i, to make utility of u, the rest of the projects must contribute u-vi, 0 if u-vi<0
            needed_util = max(u - vi, 0)
            # if we've already compute the table elements we need, we can compute T[i][u]
            if T[t + 1][needed_util] is not None and T[i - 1][u] is not None:
                T[i][u] = min(wi + T[t + 1][needed_util], T[i - 1][u])
            else:
                # we need to compute prerequisite table entries
                to_compute.append((i, u))
                if T[t + 1][needed_util] is None:
                    to_compute.append((t + 1, needed_util))
                if T[i - 1][u] is None:
                    to_compute.append((i - 1, u))
        # given T[m][r], we compare to the budget to see if we have spare capacity to achieve more utility, or if we are
        # over capacity
        if T[m][r] > b:
            upper_bound = r - 1
        else:
            lower_bound = r
    return T, upper_bound


def from_table_reversed(E, P, T, u):
    """
    Generates the set of projects that achieves u within E's budget, given a sufficiently filled dyn. prog. table
    :param E: An election
    :param P: The projects of E ordered by end point
    :param T: The reverse knapsack dynamic programming table for E
    :param u: the optimal utility we have found that we can achieve for E
    :return proj_set: A subset of E.projects that achieves utility u within E's budget
    """
    i = len(E.projects)
    proj_set = set()
    while i > 0:
        wi = P[i - 1].cost
        vi = E.approvals_by_project[P[i - 1]]
        prec_projects = compute_preceding_projects(P)
        t = prec_projects[i] + 1
        needed_util = max(u - vi, 0)
        # If item i is not in an optimal set, then adding item i mean that we would need a larger weight limit to reach
        # the same utility, so therefore if we add item i and the weight limit we need from the remaining items is not
        # more than the weight limit we require from the first i-1 items, then item i is in the optimal set
        if T[i - 1][u] < wi + T[t][needed_util]:
            i = i - 1
        else:
            proj_set.add(P[i - 1])
            i = t
            u = needed_util
    return proj_set


def interval_knapsack_projects_reversed(E):
    """
    Generates the optimal winning set for election E
    :param E: An election
    :return proj_set: The optimal project set for E
    """
    # Generate the dynamic programming table
    T, best_util = interval_knapsack_table_reversed(E)
    P = list(sorted(E.projects, key=lambda p: p.end))
    # Get the project set from the table
    proj_set = from_table_reversed(E, P, T, best_util)
    return proj_set
