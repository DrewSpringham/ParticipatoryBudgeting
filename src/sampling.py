import random
import string
import timeit
from math import ceil, log

import pandas as pd
from tqdm import trange

from src.election_instance import Election
from src.helpers import check_EJR_single_approval, is_single
from src.rules.BasicSingleEJR import basicejr
from tests.real_instances import real_instances

if __name__ == "__main__":
    # f = "../tests/pb_files/poland_wroclaw_2015_from-500.pb"
    source = real_instances()
    source_name = "real"

    for E in source:
        try:
            elections = {'election_id': [], 'voters': [], 'projects': [], 'budget': [], 'min_cost': []}
            results = {'election_id': [], 'rule_id': [], 'run_id': [], 'delta': [], 'eps': [], 'real_eps': []}

            if is_single(E):
                m = min([p.cost for p in E.projects]) + 0.0001
                elections['election_id'].append(E.election_id)
                elections['voters'].append(len(E.voters))
                elections['projects'].append(len(E.projects))
                elections['budget'].append(E.budget)
                elections['min_cost'].append(m)
                delt = 0.05
                K = len(E.projects)

                runs = 500
                for eps_i in range(60):
                    negative_samples = 0
                    real_eps_sum = 0
                    max_real_eps = 0
                    eps = (eps_i + 1) / 20
                    n = ceil(E.budget ** 2 * log(K / delt) / (2 * eps ** 2 * m ** 2))
                    if n <= len(E.voters):
                        print(f"EPSILON: {eps}\n")
                        print(f"SAMPLE SIZE {n}")
                        for i in trange(runs):

                            S = set(random.sample(list(E.voters), n))
                            subapprovals = E.approvals.copy()
                            for v in E.voters:
                                if v not in S:
                                    del subapprovals[v]
                            subelection = Election(S, E.projects, subapprovals, None, E.budget)
                            W = basicejr(subelection)
                            real_eps = check_EJR_single_approval(E, W)
                            real_eps_sum += real_eps
                            max_real_eps = max(max_real_eps, real_eps)
                            if real_eps > eps:
                                negative_samples += 1
                            results['election_id'].append(E.election_id)
                            results['rule_id'].append("BasicJR")
                            results['run_id'].append(''.join(random.choice(string.ascii_letters) for i in range(64)))
                            results['delta'].append(delt)
                            results['eps'].append(eps)
                            results['real_eps'].append(real_eps)
        finally:
            try:
                election_frame = pd.DataFrame(elections)
                res_frame = pd.DataFrame(results)
                if source_name == "random":
                    add = "_random"
                else:
                    add = ""
                election_frame.to_csv(f'elections{add}.csv', mode='a', index=False, header=False)
                res_frame.to_csv(f'results{add}.csv', mode='a', index=False, header=False)
            except PermissionError:
                t = timeit.default_timer()

                election_frame = pd.DataFrame(elections)
                res_frame = pd.DataFrame(results)
                election_frame.to_csv(f'elections_{ceil(t)}.csv', index=False, header=False)
                res_frame.to_csv(f'results_{ceil(t)}.csv', index=False, header=False)
