from src.election_instance import *

from src.helpers import compute_preceding_projects


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
    return m


def from_table(E, P, T):
    """
    Gets the project set from the partially filled dynamic programming table
    :param E: An election
    :param P: The project set of P ordered by end point
    :param T: The partially filled dynamic programming table for E
    :return:
    """
    proj_set = set()
    i = len(E.projects)
    w = E.budget
    # at each iteration, we look if we should include item i to the project set given our current weight limit w
    while i > 0:
        wi = P[i - 1].cost
        prec_projects = compute_preceding_projects(P)
        k = prec_projects[i] + 1
        # if the weight of project i is greater than our remaining weight limit, then we can't add it, so we then look
        # at project i-1
        # also, if the utility we get from not adding it and using all items up to i-1 is more than we get from adding
        # it and only using items up to k, we won't add it
        if w < wi or T[i - 1][w] > T[k][w - wi] + E.approvals_by_project[P[i - 1]]:
            i = i - 1
        # if we can add it and we get more utility from adding it, we'll add it, and update the weight limit
        else:
            proj_set.add(P[i - 1])
            i = k
            w = w - wi

    return proj_set


def interval_knapsack_projects(E):
    """
    Create the optimal project set for election E
    :param E: An election
    :return: A subsset of projects of E that optimise utiliatrian welfare for E
    """
    # Generate the dynamic programming table
    T = interval_knapsack_table(E)
    P = list(sorted(E.projects, key=lambda p: p.end))
    proj_set = from_table(E, P, T)
    return proj_set
