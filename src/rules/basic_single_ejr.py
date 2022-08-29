from src.election_instance import Election
from src.sampling import is_single


def basicejr(E: Election):
    """
    Generates the minimal EJR project set for a single approval election
    :param E: A single approval election
    :return W: A minimal EJR winning set for E
    """
    if not is_single(E):
        raise ValueError("Election needs to be single")
    # For each project, check if the number of people that approve is sufficiently large such that exclduing the
    # project would make the project set no longer EJR
    W = [p for p in E.projects if E.approvals_by_project[p] >= p.cost / E.budget * len(E.voters)]
    return set(W)
