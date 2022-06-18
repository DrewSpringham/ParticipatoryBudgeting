class Project:
    def __init__(self, start, size, cost):
        self.start = start
        self.size = size
        self.cost = cost

    @property
    def end(self):
        return self.start + self.size


class Election:

    def __init__(self, voters, projects, approvals, budget=1):
        """

        :param voters: A set of voters
        :param projects: A set of Projects
        :param approvals: A dictionary, indexed by voters and containing set of Projects as values
        :param budget:
        """
        self.approvals = approvals
        self.voters = voters
        self.projects = projects
        self.budget = budget
