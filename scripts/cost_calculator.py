# case = {'skills': list of skills names, 'candidates': list of candidates names,
# 'positions': list of positions ids, 'candidates_skills': [lists of skills for every candidate],
# 'position_skills': [list od skills needed for every position]}

def calculate_cost(case, solution_matrix):
    k = len(case['skills'])
    cost = 0
    for position_idx, candidates in enumerate(solution_matrix):
        for skill_idx in range (k):
            curr_cost = case['position_skills'][position_idx][skill_idx]
            for candidate_idx, chosen in enumerate(candidates):
                if chosen == 1:
                    curr_cost -= case['candidates_skills'][candidate_idx][skill_idx]
            if curr_cost < 0:
                curr_cost = 0
            cost += curr_cost
    return cost