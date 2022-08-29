from more_itertools import powerset


def verify_outcome(E, W):
    """
    Check that a winning set if valid for E
    :param E: An election
    :param W: A subset of projects of E
    :return: Bool indicating if W is valid for E
    """
    # if W is over budget, it is not valid
    if sum([p.cost for p in W]) > E.budget:
        return False
    # For each pair of projects, check they dont overlap. Could be more efficient in this but don't need to be
    for p in W:
        for q in W:
            if p != q:
                # Projects overlap iff one's start exists within the others interval
                if q.start <= p.start <= q.end or p.start <= q.start <= p.end:
                    return False
    return True


def check_optimality(E, W):
    """
    Brute force check the utilitarian welfare optimality of W
    :param E: An election
    :param W: A winning set for E
    :return: if W is utilitarian welfare optimal
    """
    max_approvals = 0
    # For every possible subset of projects
    for s in powerset(E.projects):
        # If the subset would be a valid outcome
        if verify_outcome(E, s):
            # Check that it does not achieve more utility than our winning set
            total_approvals = sum([E.approvals_by_project[v] for v in s])
            if total_approvals > max_approvals:
                max_approvals = total_approvals
    achieved_value = sum([E.approvals_by_project[p] for p in W])
    return max_approvals == achieved_value


def compute_preceding_projects(P):
    """
    Compute a map from projects to the index of the project that lies wholly to the left of it
    :param P: The set of projects sorted by end point
    :return: A dictionary from projects to the index of the  project that lies wholly to the left of it
    """
    m = len(P)
    prec_projects = {}
    for j in range(m + 1):
        found = False
        # Could make this more efficient with a binary search since P is sorted by end point, but don't need to
        # Iterate backwards from project j until we find the project that lies wholly to the left of it, so that
        # projects end is before project i's start
        for k in range(j - 1, -2, -1):
            if P[k].end < P[j - 1].start:
                prec_projects[j] = k
                found = True
                break
        # If we don't find it, its because no project lies to the left of it, so we assign it index -1
        if not found:
            prec_projects[j] = -1
    return prec_projects
