from sample_case import get_sample_case
from cost_calculator import calculate_cost
from solver import Algorithm
import matplotlib.pyplot as plt

min_results = []
avg_results = []
max_results = []

m = 15
n = 10
k = 5
N = 10

for r in range(1, 11):
    results = []
    for i in range(N):
        sample_case = get_sample_case(k, m, n)
        Algo = Algorithm(sample_case, radius=r)
        Algo.step()
        cost = calculate_cost(Algo.case, Algo.best_solution)
        for j in range(50):
            Algo.step()
        new_cost = calculate_cost(Algo.case, Algo.best_solution)
        results.append((cost-new_cost)/cost*100)
    min_results.append(min(results))
    avg_results.append(sum(results) / N)
    max_results.append(max(results))

r = [i for i in range(1, 11)]
print(min_results)
print(avg_results)
print(max_results)
plt.plot(r, min_results)
plt.plot(r, avg_results)
plt.plot(r, max_results)
plt.legend(['min', 'average', 'max'])
plt.xlabel('radius')
plt.ylabel('improvement [%]')
plt.title('k = {}, m = {}, n = {}'.format(k, m, n))
plt.show()