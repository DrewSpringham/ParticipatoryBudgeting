import math
import sys

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
    """
    Compute the knapsack table for E using the standard knapsack table format: rows representing how many projects
    we are considering, columns representing weight limit
    :param E:
    :return m: the (partial) knapsack table, with sufficient entries filled to compute optimal project set
    """
    # number of projects
    n = len(E.projects)
    # Projects asc. sorted by end point
    P = list(sorted(E.projects, key=lambda p: p.end))
    W = E.budget
    # set up table
    m = [[None for _ in range(W + 1)] for _ in range(n + 1)]
    # If we consider no projects, the best utility we can achieve is 0, so weight is irrelevant
    for w in range(W + 1):
        m[0][w] = 0
    # We compute table entries on demand instead of the whole table, so we set up a stack
    # we wish to compute the (n,W) entry, as this corresponds to finding the best utility from all n projects and
    # weight limit of W
    to_compute = [(n, W)]
    # We compute for every project p the project q whose endpoint is furthest to the right of p and not
    # overlapping with p
    prec_project = compute_preceding_projects(P)
    # We shall stop once we have computed all table entries we need to compute
    while len(to_compute) > 0:
        i, w = to_compute.pop()
        proj_index = i - 1
        proj = P[proj_index]
        wi = proj.cost
        # prec_index is the index of P of the precding project
        prec_index = prec_project[i]
        # if, for this weight limit w, we could ever include the i'th project in the set, the optimal value is the same
        # as not considering project i
        if wi > w:
            # we may not have already computed this value, so we'll put the current (i,w) back on the stack and add
            # the compuation of (i-1,w) on the stack
            if m[i - 1][w] is None:
                to_compute.append((i, w))
                to_compute.append((i - 1, w))
            else:
                m[i][w] = m[i - 1][w]
        else:
            util = E.approvals_by_project[proj]
            if m[i - 1][w] is not None and m[prec_index + 1][w - wi] is not None:
                m[i][w] = max(m[i - 1][w], util + m[prec_index + 1][w - wi])
            else:
                # We can't compute (i,w) yet because some computation we depend on has not been computed, so we add it
                # back to the stack so we can come back to it later
                to_compute.append((i, w))
                if m[i - 1][w] is None:
                    to_compute.append((i - 1, w))
                if m[prec_index + 1][w - wi] is None:
                    to_compute.append((prec_index + 1, w - wi))
    print(sum([sys.getsizeof(l) for l in m]))
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
    m, best_util = interval_knapsack_table_reversed(E)
    n = len(E.projects)
    P = list(sorted(E.projects, key=lambda p: p.end))
    proj_set = from_table_reversed(E, P, m, n, best_util)
    return proj_set
