from sample_case import get_sample_case
from sample_sol import gen_sample_solution, gen_sample_sol_mn
from cost_calculator import calculate_cost

if __name__ == '__main__':
    sample_case = get_sample_case(5, 6, 3)
    print(sample_case)
    sample_sol, sample_sol_matrix = gen_sample_solution(sample_case)
    print(sample_sol)
    print(sample_sol_matrix)
    sample_sol_v1 = gen_sample_sol_mn(14, 6)
    print(sample_sol_v1)
    print(calculate_cost(sample_case, sample_sol_matrix))

