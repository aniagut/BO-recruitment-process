from sample_case import get_sample_case
from sample_sol import get_solution
import sys
import solver

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Invalid number of arguments!")
        exit(-1)
    k = int(sys.argv[1])
    m = int(sys.argv[2])
    n = int(sys.argv[3])
    sample_case = get_sample_case(k, m, n)
    Algo = solver.Algorithm(sample_case, radius=7)
    for i in range(66):
        Algo.step()

    print(get_solution(Algo.case, Algo.best_solution))

