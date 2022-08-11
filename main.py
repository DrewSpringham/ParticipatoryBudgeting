from src.rules.interval_knapsack import *

voters = [i for i in range(1, 8)]
p1 = Project(0, 0.2, 3)
p2 = Project(0, 0.5, 1)
p3 = Project(0.4, 0.2, 4)
p4 = Project(0.45, 0.35, 7)
p5 = Project(0.7, 0.3, 2)
projects = [p1, p2, p3, p4, p5]
approvals = {1: set([p1, p2, p3, p4, p5]), 2: set([p1, p3, p4, p5]), 3: set([p1, p3, p4]), 4: set([p3, p4]),
             5: set([p4]), 6: set([p4]), 7: set([p4])}
E = Election(voters, projects, approvals, None, budget=9)
print(interval_knapsack_projects(E))
