import random
import string
from collections import defaultdict


class Project:
    """
    Defines a locational project
    """

    def __init__(self, start, size, cost):
        """
        Creates a locational project
        :param start: Start position on the interval
        :param size: The size (width) of the project
        :param cost: The cost of the project
        """
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

    def __init__(self, voters, projects, approvals, election_id=None, budget=1):
        """
        Creates an election
        :param election_id: An identifier for the election. Optional, but useful for testing
        :param voters: A set of voters
        :param projects: A set of Projects
        :param approvals: A dictionary, indexed by voters and containing set of Projects as values
        :param budget: The budget of the election
        """

        self.approvals = approvals
        self.voters = voters
        self.projects = projects
        self.budget = budget
        # If we don't have an id, create a random 64 length string
        if election_id is None:
            self.election_id = ''.join(random.choice(string.ascii_letters) for i in range(64))
        else:
            self.election_id = election_id

    @property
    def approvals_by_project(self):
        """
        Generates a dictionary that takes projects to the total number of voters that approve it. Dictionary is cached,
        so only generated once
        :return: dictionary that takes projects to the total number of voters that approve it.
        """
        if self._approvals_by_project is not None:
            return self._approvals_by_project
        else:
            total_project_approval = defaultdict(int)
            # Iterate over voters and add one to the count of each project the voter approves
            for v in self.voters:
                for p in self.approvals[v]:
                    total_project_approval[p] += 1
            self._approvals_by_project = total_project_approval
            return total_project_approval
