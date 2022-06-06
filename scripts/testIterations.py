from sample_case import get_sample_case
from cost_calculator import calculate_cost
from solver import Algorithm
import matplotlib.pyplot as plt

min_results = []
avg_results = []
max_results = []

m = 10
n = 10
N = 10

for iter in range(1, 51):
    results = []
    print("ITER")
    print(iter)
    for i in range(N):
        sample_case = get_sample_case(5, m, n)
        Algo = Algorithm(sample_case, radius=7)
        Algo.step()
        cost = calculate_cost(Algo.case, Algo.best_solution)
        for j in range(iter):
            Algo.step()
        new_cost = calculate_cost(Algo.case, Algo.best_solution)
        results.append((cost-new_cost)/cost*100)
    min_results.append(min(results))
    avg_results.append(sum(results) / N)
    max_results.append(max(results))

x = [i for i in range(1, 51)]
print(min_results)
print(avg_results)
print(max_results)
plt.plot(x, min_results)
plt.plot(x, avg_results)
plt.plot(x, max_results)
plt.legend(['min', 'average', 'max'])
plt.xlabel('number of iterations')
plt.ylabel('improvement [%]')
plt.show()