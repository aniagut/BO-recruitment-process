from sample_case import get_sample_case
from sample_sol import get_solution, gen_sample_sol_mn
from cost_calculator import calculate_cost

if __name__ == '__main__':
    m = 6
    n = 3
    sample_case = get_sample_case(5, m, n)
    print(sample_case)
    sample_sol_matrix = gen_sample_sol_mn(m, n)
    sample_sol = get_solution(sample_case, sample_sol_matrix)
    print(sample_sol)
    print(sample_sol_matrix)

    sample_sol_v1 = gen_sample_sol_mn(14, 6)
    print(sample_sol_v1)
    print(calculate_cost(sample_case, sample_sol_matrix))

