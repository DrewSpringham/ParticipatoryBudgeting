from src.election_instance import Election
from src.rules.interval_knapsack import interval_knapsack_projects
from tests.random_instances import random_project


def convert(filepath):
    meta = {}
    projects = set()
    voters = set()
    phase = 0
    approvals = {}
    project_ids = {}
    with open(filepath, encoding="utf8") as f:
        lines = [l.strip() for l in f.readlines()]

        line_number = 2
        while lines[line_number] != "PROJECTS":
            l = lines[line_number].split(";")
            meta[l[0]] = l[1]
            line_number += 1

        line_number += 1
        l = lines[line_number].split(";")
        id_index = l.index("project_id")
        cost_index = l.index("cost")
        line_number += 1
        while lines[line_number] != "VOTES":
            l = lines[line_number].split(";")
            cost = int(l[cost_index])
            p = random_project(cost, cost)
            projects.add(p)
            project_ids[l[id_index]] = p
            line_number += 1

        line_number += 1
        l = lines[line_number].split(";")
        id_index = l.index("voter_id")
        vote_index = l.index("vote")
        line_number += 1
        for line in lines[line_number:]:
            l = line.split(";")
            voter = l[id_index]
            votes = set(l[vote_index].split(","))
            approval = set([project_ids[v] for v in votes])
            approvals[voter] = approval
            voters.add(voter)
    if meta["vote_type"] != "approval":
        raise ValueError("Cannot operate on non-approval elections!")
    return Election(voters, projects, approvals, int(meta["budget"]))


E = convert("pb_files/poland_warszawa_2017_miedzeszyn.pb")
print(interval_knapsack_projects(E))
