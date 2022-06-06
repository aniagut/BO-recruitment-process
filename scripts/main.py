from sample_case import get_sample_case
from cost_calculator import calculate_cost
from solver import Algorithm
import random

if __name__ == '__main__':
    random.seed(23)

    n = 30
    m = 10
    k = 4
    n_iter = 50

    sample_case = get_sample_case(k, n, m)
    print(sample_case)

    Algo = Algorithm(sample_case, radius=7)
    Algo.step()
    print(calculate_cost(Algo.case, Algo.best_solution))
    for i in range(n_iter):
        Algo.step()

    print(calculate_cost(Algo.case, Algo.best_solution))
