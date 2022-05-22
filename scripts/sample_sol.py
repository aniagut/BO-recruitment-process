import random
# sample case = {'skills': list of skills names, 'candidates': list of candidates names,
# 'positions': list of positions ids, 'candidates_skills': [lists of skills for every candidate],
# 'position_skills': [list od skills needed for every position]}
def get_solution(case, sol_mn):
    solution = dict()
    for position_index, position in enumerate(case['positions']):
        solution[position] = []
        for candidate_index, candidate in enumerate(case['candidates']):
            if sol_mn[position_index][candidate_index] == 1:
                solution[position].append(candidate)
    return solution

def gen_sample_sol_mn(m: int, n: int):
    solution_matrix = [[0 for _ in range (m)] for _ in range (n)]
    for idx in range(m):
        sol_idx = random.randint(0, n-1)
        solution_matrix[sol_idx][idx] = 1
    return solution_matrix