def verify_outcome(E, P):
    if sum([p.cost for p in P]) > E.budget:
        return False
    for p in P:
        for q in P:
            if p != q:
                if q.start <= p.start <= q.end or p.start <= q.start <= p.end:
                    return False
    return True
