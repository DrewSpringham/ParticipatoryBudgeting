from src.election_instance import Election


# TODO:document

def naive_from_table(E, P, m, i, w):
    if i == 0:
        return set()
    wi = P[i - 1].cost
    if wi > w:
        return naive_from_table(E, P, m, i - 1, w)
    for k in range(i - 1, -2, -1):
        if P[k].end < P[i - 1].start:
            break
    k = k + 1
    if m[i - 1][w] > m[k][w - wi] + E.approvals_by_project[P[i - 1]]:
        proj_set = naive_from_table(E, P, m, i - 1, w)
    else:
        proj_set = naive_from_table(E, P, m, k, w - wi)
        proj_set.add(P[i - 1])
    return proj_set


def naive_interval_knapsack_table(E: Election):
    n = len(E.projects)
    P = list(sorted(E.projects, key=lambda p: p.end))
    W = E.budget
    # set up table
    m = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    for j in range(n):
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


def naive_interval_knapsack_score(E: Election):
    i = len(E.projects)
    W = E.budget
    m = naive_interval_knapsack_table(E)
    return m[i][W]


def naive_interval_knapsack_projects(E):
    m = naive_interval_knapsack_table(E)
    i = len(E.projects)
    W = E.budget
    P = list(sorted(E.projects, key=lambda p: p.end))
    proj_set = naive_from_table(E, P, m, i, W)
    return proj_set
