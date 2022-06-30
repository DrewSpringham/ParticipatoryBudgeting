import os

from src.election_instance import Election, Project
from tests.random_instances import random_project


def convert_to_election(filepath):
    meta = {}
    projects = set()
    voters = set()
    approvals = {}
    project_ids = {}
    with open(filepath, encoding="utf8") as f:
        lines = [l.strip() for l in f.readlines()]

        line_number = 2
        while lines[line_number] != "PROJECTS":
            l = lines[line_number].replace(" ", "").split(";")
            meta[l[0]] = l[1]
            line_number += 1
        try:
            comma = meta['budget'].index(",")
            meta['budget'] = meta['budget'][:comma]
        except ValueError:
            pass
        line_number += 1
        l = lines[line_number].replace(" ", "").split(";")
        id_index = l.index("project_id")
        cost_index = l.index("cost")
        locational = True
        try:
            start_index = l.index("start")
            end_index = l.index("end")
        except ValueError:
            locational = False
        line_number += 1
        while lines[line_number] != "VOTES":
            l = lines[line_number].split(";")
            cost = int(l[cost_index])
            if locational:
                start = float(l[start_index])
                end = float(l[end_index])
                p = Project(start, end - start, cost)
            else:
                p = random_project(cost, cost)
            projects.add(p)
            project_ids[l[id_index]] = p
            line_number += 1

        line_number += 1
        l = lines[line_number].replace(" ", "").split(";")
        id_index = l.index("voter_id")
        vote_index = l.index("vote")
        line_number += 1
        for line in lines[line_number:]:
            l = line.replace(" ", "").split(";")
            voter = l[id_index]
            votes = set(l[vote_index].split(","))
            approval = set([project_ids[v] for v in votes])
            approvals[voter] = approval
            voters.add(voter)
    if meta["vote_type"] != "approval":
        raise ValueError("Cannot operate on non-approval elections!")
    return Election(voters, projects, approvals, int(meta["budget"]))


def convert_to_file(E, filepath):
    lines = []
    lines.append("META")
    lines.append("key; value")
    lines.append(f"num_projects; {len(E.projects)}")
    lines.append(f"num_votes; {len(E.voters)}")
    lines.append(f"budget; {E.budget}")
    lines.append(f"vote_type; approval")
    lines.append("PROJECTS")
    lines.append("project_id; cost; start; end")
    project_ids = {}
    for id_counter, p in enumerate(E.projects):
        project_ids[p] = id_counter
        lines.append(f"{id_counter}; {p.cost}; {p.start}; {p.end}")
    lines.append("VOTES")
    lines.append("voter_id; vote")
    for id_counter, v in enumerate(E.voters):
        approved = [str(project_ids[p]) for p in E.approvals[v]]
        votes = ', '.join(approved)
        lines.append(f"{id_counter}; {votes}")
    with open(filepath, 'w') as f:
        for l in lines:
            f.write(f"{l}\n")


def convert_real_instances():
    read_directory = "pb_files"
    write_directory = "pb_files_loc"
    for filename in os.listdir(read_directory):
        f = os.path.join(read_directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            E = convert_to_election(f)
            convert_to_file(E, write_directory + "/" + filename)


convert_real_instances()
