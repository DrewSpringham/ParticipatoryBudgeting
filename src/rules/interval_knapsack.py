import math

from src.election_instance import *


# TODO: divisor not being computed properly? Rework this
def reduce_weights(E):
    divisor = math.gcd(*[p.cost for p in E.projects])
    new_projects = set()
    old_to_new = {}
    new_approvals = {}
    for p in E.projects:
        new_p = Project(p.start, p.size, p.cost // divisor)
        new_projects.add(p)
        old_to_new[p] = new_p
    for v in E.voters:
        new_approvals[v] = set([old_to_new[p] for p in E.approvals[v]])
    new_budget = E.budget // divisor

    return Election(E.voters, new_projects, new_approvals, new_budget)


def compute_preceding_projects(P):
    n = len(P)
    j_to_k = {}
    for j in range(n + 1):
        found = False
        for k in range(j - 1, -2, -1):
            if P[k].end < P[j - 1].start:
                j_to_k[j] = k
                found = True
                break
        if not found:
            j_to_k[j] = -1
    return j_to_k


def interval_knapsack_table(E: Election):
    n = len(E.projects)
    P = list(sorted(E.projects, key=lambda p: p.end))
    W = E.budget
    # set up table
    m = [[None for _ in range(W + 1)] for _ in range(n + 1)]
    for w in range(W + 1):
        m[0][w] = 0
    to_compute = [(n, W)]
    j_to_k = compute_preceding_projects(P)
    while len(to_compute) > 0:
        j, w = to_compute.pop()
        wi = P[j - 1].cost
        k = j_to_k[j]
        if wi > w:
            if m[j - 1][w] is None:
                to_compute.append((j, w))
                to_compute.append((j - 1, w))
            else:
                m[j][w] = m[j - 1][w]
        else:
            vi = E.approvals_by_project[P[j - 1]]
            if m[j - 1][w] is not None and m[k + 1][w - wi] is not None:
                m[j][w] = max(m[j - 1][w], vi + m[k + 1][w - wi])
            else:
                to_compute.append((j, w))
                if m[j - 1][w] is None:
                    to_compute.append((j - 1, w))
                if m[k + 1][w - wi] is None:
                    to_compute.append((k + 1, w - wi))
    return m


def from_table(E, P, m, i, w):
    if i == 0:
        return set()
    wi = P[i - 1].cost
    if wi > w:
        return from_table(E, P, m, i - 1, w)
    for k in range(i - 1, -2, -1):
        if P[k].end < P[i - 1].start:
            break
    k = k + 1
    if m[i - 1][w] > m[k][w - wi] + E.approvals_by_project[P[i - 1]]:
        proj_set = from_table(E, P, m, i - 1, w)
    else:
        proj_set = from_table(E, P, m, k, w - wi)
        proj_set.add(P[i - 1])
    return proj_set


def interval_knapsack_projects(E):
    m = interval_knapsack_table(E)
    i = len(E.projects)
    W = E.budget
    P = list(sorted(E.projects, key=lambda p: p.end))
    proj_set = from_table(E, P, m, i, W)
    return proj_set


def interval_knapsack_table_reversed(E: Election):
    n = len(E.projects)
    v = len(E.voters)
    P = list(sorted(E.projects, key=lambda p: p.end))
    W = E.budget
    # set up table
    m = [[None for _ in range(1 + n * v)] for _ in range(n + 1)]
    j_to_k = compute_preceding_projects(P)
    for u in range(1 + n * v):
        m[0][u] = math.inf
    for i in range(n + 1):
        m[i][0] = 0
    for i in range(1, n + 1):
        for u in range(1, 1 + n * v):
            vi = E.approvals_by_project[P[i - 1]]
            wi = P[i - 1].cost
            k = j_to_k[i]
            needed_util = max(u - vi, 0)
            m[i][u] = min(wi + m[k + 1][needed_util], m[i - 1][u])

    return m


def from_table_reversed(E, P, m, i, u):
    if i == 0:
        return set()
    wi = P[i - 1].cost
    vi = E.approvals_by_project[P[i - 1]]
    j_to_k = compute_preceding_projects(P)
    k = j_to_k[i]
    needed_util = max(u - vi, 0)
    if m[i - 1][u] < wi + m[k + 1][needed_util]:
        proj_set = from_table_reversed(E, P, m, i - 1, u)
    else:
        proj_set = from_table_reversed(E, P, m, k + 1, needed_util)

        proj_set.add(P[i - 1])
    return proj_set


def interval_knapsack_projects_reversed(E):
    m = interval_knapsack_table_reversed(E)
    n = len(E.projects)
    v = len(E.voters)
    W = E.budget
    P = list(sorted(E.projects, key=lambda p: p.end))
    best_util = 0
    for u in range(1 + n * v):
        if m[n][u] <= W:
            best_util = u
    proj_set = from_table_reversed(E, P, m, n, best_util)
    return proj_set
