from src.election_instance import *


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


def interval_knapsack_table(E: Election):
    n = len(E.projects)
    P = list(sorted(E.projects, key=lambda p: p.end))
    W = E.budget
    # set up table
    m = [[None for _ in range(W + 1)] for _ in range(n + 1)]
    for w in range(W + 1):
        m[0][w] = 0
    to_compute = [(n, W)]
    while len(to_compute) > 0:
        j, w = to_compute.pop()
        wi = P[j - 1].cost
        for k in range(j - 1, -2, -1):
            if P[k].end < P[j - 1].start:
                break
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


def interval_knapsack_score(E: Election):
    i = len(E.projects)
    W = E.budget
    m = interval_knapsack_table(E)
    return m[i][W]


def interval_knapsack_projects(E):
    m = interval_knapsack_table(E)
    i = len(E.projects)
    W = E.budget
    P = list(sorted(E.projects, key=lambda p: p.end))
    proj_set = from_table(E, P, m, i, W)
    return proj_set
