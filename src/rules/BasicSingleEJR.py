from src.election_instance import Election
from src.helpers import is_single
from tests.pabulib_converter import convert_to_election


def basicejr(E: Election):
    if not is_single(E):
        raise ValueError("Election needs to be single")
    W = set()
    running_cost = 0
    for p in E.projects:
        if E.approvals_by_project[p] >= p.cost / E.budget * len(E.voters):
            W.add(p)
            running_cost += p.cost
    return W


if __name__ == "__main__":
    f = "../../tests/pb_files/poland_wroclaw_2015_from-500.pb"
    E = convert_to_election(f, None)
    print(basicejr(E))
