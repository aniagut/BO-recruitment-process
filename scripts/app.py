from sample_sol import get_solution
import sys
import solver
import json

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Invalid number of arguments!")
        exit(-1)
    json_file = sys.argv[1]
    with open(json_file) as f:
        sample_case = json.load(f)
    Algo = solver.Algorithm(sample_case, radius=7)
    for i in range(66):
        Algo.step()
    print(get_solution(Algo.case, Algo.best_solution))

