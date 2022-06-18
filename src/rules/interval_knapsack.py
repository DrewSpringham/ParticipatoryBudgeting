from collections import defaultdict

from src.election_instance import *


def interval_knapsack(E: Election):
    total_project_approval = defaultdict(int)
    for v in E.voters:
        for p in E.approvals[v]:
            total_project_approval[p] += 1

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
                vi = total_project_approval[P[j]]
                m[j + 1][w] = max(m[j][w], vi + m[k + 1][w - wi])
    return m[i][W]
