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
    i = len(E.projects)
    P = list(sorted(E.projects, key=lambda p: p.end))
    W = E.budget
    # set up table
    m = [[0 for w in range(W + 1)] for j in range(i + 1)]
    # for j=0, we have m[0,w]=0
    for w in range(W + 1):
        m[0][w] = 0
    for j in range(i):
        for k in range(j, -2, -1):
            if P[k].end < P[j].start:
                break
        wi = P[j].cost
        for w in range(W + 1):
            if wi > w:
                m[j + 1][w] = m[j][w]
            else:
                vi = E.approvals_by_project[P[j]]
                m[j + 1][w] = max(m[j][w], vi + m[k + 1][w - wi])
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
