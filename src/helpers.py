from more_itertools import powerset


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
