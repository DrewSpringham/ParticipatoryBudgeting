from collections import defaultdict


class Project:
    def __init__(self, start, size, cost):
        self.start = start
        self.size = size
        self.cost = cost

    def __repr__(self):
        return '{start}/{end}/{cost}'.format(start=self.start, end=self.end, cost=self.cost)

    @property
    def end(self):
        return self.start + self.size


class Election:
    _approvals_by_project = None

    def __init__(self, voters, projects, approvals, election_id, budget=1):
        """

        :param election_id:
        :param voters: A set of voters
        :param projects: A set of Projects
        :param approvals: A dictionary, indexed by voters and containing set of Projects as values
        :param budget:
        """
        self.election_id = election_id
        self.approvals = approvals
        self.voters = voters
        self.projects = projects
        self.budget = budget

    @property
    def approvals_by_project(self):
        if self._approvals_by_project is not None:
            return self._approvals_by_project
        else:
            total_project_approval = defaultdict(int)
            for v in self.voters:
                for p in self.approvals[v]:
                    total_project_approval[p] += 1
            self._approvals_by_project = total_project_approval
            return total_project_approval
