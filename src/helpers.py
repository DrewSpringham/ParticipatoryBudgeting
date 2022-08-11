import math

from more_itertools import powerset

from src.election_instance import Project, Election


def verify_outcome(E, P):
    if sum([p.cost for p in P]) > E.budget:
        return False
    for p in P:
        for q in P:
            if p != q:
                if q.start <= p.start <= q.end or p.start <= q.start <= p.end:
                    return False
    return True


def check_optimality(E, P):
    max_approvals = 0
    max_project_set = None
    for s in powerset(E.projects):
        if verify_outcome(E, s):
            total_approvals = sum([E.approvals_by_project[v] for v in s])
            if total_approvals > max_approvals:
                max_approvals = total_approvals
                max_project_set = s
    achieved_value = sum([E.approvals_by_project[p] for p in P])
    return max_approvals == achieved_value


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
