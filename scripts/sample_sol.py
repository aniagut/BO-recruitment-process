import random
# sample case = {'skills': list of skills names, 'candidates': list of candidates names,
# 'positions': list of positions ids, 'candidates_skills': [lists of skills for every candidate],
# 'position_skills': [list od skills needed for every position]}
def get_solution(case, sol_mn):
    n = len(case['positions'])
    m = len(case['candidates'])
    solution = dict()
    for position in case['positions']:
        solution[position] = []
    for candidate_idx, candidate in enumerate(case['candidates']):
        idx = random.randint(0,n-1)
        solution[case['positions'][idx]].append(candidate)
        sol_mn[idx][candidate_idx] = 1
    return solution

def gen_sample_sol_mn(m: int, n: int):
    solution_matrix = [[0 for _ in range (m)] for _ in range (n)]
    for idx in range(m):
        sol_idx = random.randint(0, n-1)
        solution_matrix[sol_idx][idx] = 1
    return solution_matrix