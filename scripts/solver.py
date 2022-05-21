import random
from sample_case import get_sample_case
from sample_sol import gen_sample_sol_mn, get_solution

'''
Classes
'''
class Bee:
    def __init__(self, case, name, solution):
        self.case = case
        self.name = name
        self.position = solution

    def move(self):
        new_position = gen_new_sol_m(self.position)
        if True:
            self.position = new_position


class Neighbourhood:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def shrink(self):
        pass

    def abandon(self):
        pass


class Algorithm:
    def __init__(self, bees, nb, nrb, stlim, case):
        self.n = len(case['positions'])
        self.m = len(case['candidates'])

        self.nb = nb
        self.nrb = nrb
        self.stlim = stlim
        self.case = case

        # Inicjalizacja
        self.bees = []
        self.hoods = []
        for i in range(bees):
            self.bees.append(gen_sample_sol_mn(m, n))

    def step(self):
        for bee in self.bees:
            bee.move


'''
Example
'''
n = 6
m = 3
sample_case = get_sample_case(5, n, m)

sample_sol_matrix = gen_sample_sol_mn(n, m)
print(sample_sol_matrix)
print(get_solution(sample_case, sample_sol_matrix))

seed = 100
random.seed(seed)


def gen_new_sol_m(case, sol_m):
    n = len(case['positions'])
    m = len(case['candidates'])
    # get random worker and assign him a random different position
    worker = random.choice(range(m))
    current_position = None
    for i in range(len(sol_m)):
        if sol_m[i][worker] == 1:
            current_position = i
            break
    available_positions = [i for i in range(n) if i != current_position]
    new_position = random.choice(available_positions)
    print(worker, current_position, new_position)
    new_matrix = [[sol_m[j][i] for i in range(m)] for j in range(n)]
    new_matrix[current_position][worker] = 0
    new_matrix[new_position][worker] = 1
    return new_matrix


new_matrix = gen_new_sol_m(sample_case, sample_sol_matrix)
print(new_matrix)
print(get_solution(sample_case, new_matrix))
