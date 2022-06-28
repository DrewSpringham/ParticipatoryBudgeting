from src.election_instance import Election
from tests.random_instances import random_project


def convert(filepath):
    meta = {}
    project_ids = {}
    voters = set()
    phase = 0
    approvals = {}
    projects = set()
    with open(filepath, encoding="utf8") as f:
        lines = f.readlines()

        for l in lines:
            if phase == 0:
                if
                    if l != "PROJECTS\n":
                        splitted = l.split(";")
                        if len(splitted) == 2:
                            meta[splitted[0]] = splitted[1]
                    else:
                        phase = 1
            elif phase == 1:
                if l != "VOTES\n":
                    splitted = l.split(";")
                    if splitted[0] != "project_id":
                        cost = int(splitted[1])
                        new_project = random_project(cost, cost)
                        projects.add(new_project)
                        project_ids[splitted[0]] = new_project
                else:
                    phase = 2
            elif phase == 2:
                splitted = l.split(";")
                if splitted[0] != "voter_id":
                    voters.add(splitted[0])
                    votes = splitted[1].split(',')
                    print(votes)
                    cost = int(splitted[1])
                    new_project = random_project(cost, cost)
                    projects.add(new_project)
                    project_ids[splitted[0]] = new_project
    if meta["vote_type"] != "approval\n":
        raise ValueError("Cannot operate on non-approval elections!")
    return Election(voters, projects, approvals, meta["budget"])


convert("pb_files/poland_warszawa_2017_miedzeszyn.pb")
