from sample_case import get_sample_case
from cost_calculator import calculate_cost
from solver import Algorithm
import matplotlib.pyplot as plt

min_results = []
avg_results = []
max_results = []

m = 10
N = 10

for n in range(2, 20):
    results = []
    for i in range(N):
        sample_case = get_sample_case(5, m, n)
        Algo = Algorithm(sample_case, radius=7)
        Algo.step()
        cost = calculate_cost(Algo.case, Algo.best_solution)
        for j in range(50):
            Algo.step()
        new_cost = calculate_cost(Algo.case, Algo.best_solution)
        results.append((cost-new_cost)/cost*100)
    min_results.append(min(results))
    avg_results.append(sum(results) / N)
    max_results.append(max(results))

n = [i for i in range(2, 20)]
print(min_results)
print(avg_results)
print(max_results)
plt.plot(n, min_results)
plt.plot(n, avg_results)
plt.plot(n, max_results)
plt.legend(['min', 'average', 'max'])
plt.xlabel('n')
plt.ylabel('improvement [%]')
plt.title('m = {}'.format(m))
plt.show()