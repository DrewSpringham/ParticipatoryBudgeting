import math

from src.election_instance import Election
from src.helpers import compute_preceding_projects


def interval_knapsack_table_reversed(E: Election):
    n = len(E.projects)
    max_total_approvals = sum([E.approvals_by_project[p] for p in E.projects])
    P = list(sorted(E.projects, key=lambda p: p.end))
    W = E.budget
    # set up table
    m = [[None for _ in range(1 + max_total_approvals)] for _ in range(n + 1)]
    j_to_k = compute_preceding_projects(P)
    for u in range(1 + max_total_approvals):
        m[0][u] = math.inf
    for i in range(n + 1):
        m[i][0] = 0
    lower_bound = 0
    upper_bound = max_total_approvals
    while lower_bound < upper_bound:
        l = (lower_bound + upper_bound + 1) // 2
        to_compute = [(n, l)]
        while len(to_compute) > 0:
            i, u = to_compute.pop()
            vi = E.approvals_by_project[P[i - 1]]
            wi = P[i - 1].cost
            k = j_to_k[i]
            needed_util = max(u - vi, 0)
            if m[k + 1][needed_util] is not None and m[i - 1][u] is not None:
                m[i][u] = min(wi + m[k + 1][needed_util], m[i - 1][u])
            else:
                to_compute.append((i, u))
                if m[k + 1][needed_util] is None:
                    to_compute.append((k + 1, needed_util))
                if m[i - 1][u] is None:
                    to_compute.append((i - 1, u))

        if m[n][l] > W:
            upper_bound = l - 1
        else:
            lower_bound = l

    return m, upper_bound


def from_table_reversed(E, P, m, i, u):
    proj_set = set()
    while i > 0:
        wi = P[i - 1].cost
        vi = E.approvals_by_project[P[i - 1]]
        j_to_k = compute_preceding_projects(P)
        k = j_to_k[i]
        needed_util = max(u - vi, 0)
        if m[i - 1][u] < wi + m[k + 1][needed_util]:
            i = i - 1
            proj_set = from_table_reversed(E, P, m, i - 1, u)
        else:
            proj_set.add(P[i - 1])
            i = k + 1
            u = needed_util
    return proj_set


def interval_knapsack_projects_reversed(E):
    m, best_util = interval_knapsack_table_reversed(E)
    n = len(E.projects)
    P = list(sorted(E.projects, key=lambda p: p.end))
    proj_set = from_table_reversed(E, P, m, n, best_util)
    return proj_set
