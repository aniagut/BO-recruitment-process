import math
import random
from sample_case import get_sample_case
import string

from sample_sol import get_solution

debug = True
def print_debug(*text):
    if debug:
        print(*text)

class Bee:
    def __init__(self, case, name):
        self.cost = None
        self.position = None
        self.case = case
        self.name = name
        self.set_random_position()
        self._evaluate()

    def __repr__(self) -> str:
        return str((self.name, self.cost))

    def set_random_position(self):
        self.position = self._gen_sample_sol_mn()

    def _gen_sample_sol_mn(self):
        """
        Wygeneruj losowe rozwiązanie.
        """
        n = len(self.case['positions'])
        m = len(self.case['candidates'])
        solution_matrix = [[0 for _ in range(m)] for _ in range(n)]
        for idx in range(m):
            sol_idx = random.randint(0, n - 1)
            solution_matrix[sol_idx][idx] = 1
        return solution_matrix

    def _gen_new_sol_m(self):
        """
        Wygeneruj nową pozycję pszczoły zmienioną o 1.
        """
        sol_m = self.position
        n = len(self.case['positions'])
        m = len(self.case['candidates'])
        # get random worker and assign him a random different position
        worker = random.choice(range(m))
        current_position = None
        for i in range(len(sol_m)):
            if sol_m[i][worker] == 1:
                current_position = i
                break
        available_positions = [i for i in range(n) if i != current_position]
        new_position = random.choice(available_positions)
        new_matrix = [[sol_m[j][i] for i in range(m)] for j in range(n)]
        new_matrix[current_position][worker] = 0
        new_matrix[new_position][worker] = 1
        return new_matrix

    def _evaluate(self):
        """
        Zaktualizuj ewaluację kosztu.
        """
        case = self.case
        solution_matrix = self.position
        k = len(case['skills'])
        cost = 0
        for position_idx, candidates in enumerate(solution_matrix):
            for skill_idx in range(k):
                curr_cost = case['position_skills'][position_idx][skill_idx]
                for candidate_idx, chosen in enumerate(candidates):
                    if chosen == 1:
                        curr_cost -= case['candidates_skills'][candidate_idx][skill_idx]
                if curr_cost < 0:
                    curr_cost = 0
                cost += curr_cost
        self.cost = cost

    def local_search(self, radius) -> bool:
        """
        Zmień pozycję pszczoły "r = neighbourhood radius" razy.
        Nie ma gwarancji, że odległość od poprzedniego rozwiązania wyniesie r, może wynieść mniej.
        Jeśli nowa pozycja jest gorsza, powróć do starej pozycji i zwróć False.
        W przeciwnym razie zostań przy nowej pozycji i zwróć True.

        Returns:
        bool: Czy pozycja się zmieniła?
        """
        old_position = self.position
        old_cost = self.cost
        for i in range(radius):
            self.position = self._gen_new_sol_m()
        self._evaluate()
        if self.cost > old_cost:
            self.position = old_position
            self.cost = old_cost
            return False
        return True

    def global_search(self):
        self.set_random_position()
        self._evaluate()


class Neighbourhood:
    def __init__(self, bee: Bee, radius, ttl):
        self.center = bee.position
        self.best_cost = bee.cost

        self.bees = [bee]
        self.radius = radius
        self.ttl = ttl

    def add_bee(self, bee: Bee):
        self.bees.append(bee)

    def shrink(self):
        self.ttl -= 1
        self.radius -= 1

    def abandon(self):
        pass


class Algorithm:
    def __init__(self,
                 case: dict,
                 ns: int = 7,
                 ne: int = 1,
                 nre: int = 2,
                 nb: int = 1,
                 nrb: int = 1,
                 ttl: int = 5,
                 radius: int = 2,
                 shrink_factor: int = 1,
                 iterations: int = 100):
        """Inicjalizacja algorytmu pszczelego.

        Parameters:
        case (dict): rozpatrywana instancja problemu
        ns (int): liczba pszczół
        ne (int): liczba elitarnych sąsiedztw
        nre (int): liczba pszczół w każdym elitarnym sąsiedztwie
        nb (int): liczba zwykłych sąsiedztw
        nrb (int): liczba pszczół w każdym zwykłych sąsiedztwie
        ttl (int): czas życia niewydajnego sąsiedztwa
        radius (int): domyślny początkowy promień sąsiedztwa, radius < m
        shrink_factor (int): o ile zmniejsza się sąsiedztwo
        iterations (int): po ilu krokach algorytm się zatrzymuje
       """
        self.case = case

        self.ns = ns
        self.ne = ne
        self.nre = nre
        self.nb = nb
        self.nrb = nrb
        self.ttl = ttl
        self.radius = radius
        self.shrink_factor = shrink_factor
        self.iterations = iterations

        self._validate()

        self.best_solution = None
        self.best_score = math.inf

        # Inicjalizacja
        self.hive: [Bee] = []
        self.bee_scouts: [Bee] = []
        self.elite_hoods: [Neighbourhood] = []
        self.good_hoods: [Neighbourhood] = []
        for i in range(ns):
            name = "".join(random.sample(string.ascii_letters, 5))
            self.hive.append(Bee(case, name))

        print_debug("Pszczoły:" +str([bee.name for bee in self.hive]))

    def _validate(self):
        n = len(self.case['positions'])
        m = len(self.case['candidates'])

        if self.radius >= m:
            raise ValueError("self.radius >= m")
        if self.ne * self.nre + self.nb + self.nrb > self.ns:
            raise ValueError("Za mało pszczół by pokryć wszystkie sąsiedztwa! Potrzeba "+str(self.ne * self.nre + self.nb + self.nrb)+" pszczół!")
        if self.ne * self.nre + self.nb + self.nrb == self.ns:
            print_debug("Nie ma wolnych pszczół-skautów!")

    def step(self):
        """
        PSZCZOŁY WRÓCIŁY DO ULA I DZIELĄ SIĘ SWOIMI WNIOSKAMI.

        ne najlepszych pszczół tworzy elitarne sąsiedztwa
        nb kolejnych pszczół tworzy nieelitarne sąsiedztwa
        pszczoły rekrutują pomocników i razem z nimi wylatują w przydzielone miejsca

        reszta pszczół zostaje skautami i przeszukuje globalną przestrzeń rozwiązań
        """
        self.hive.sort(key=lambda bee: bee.cost)

        best_solution, best_score = self.hive[0].position, self.hive[0].cost
        if best_score < self.best_score:
            print_debug("Nowy najlepszy wynik",self.hive[0].cost,"znalazła pszczoła",self.hive[0].name)
            self.best_solution = best_solution
            self.best_score = best_score

        # 1. Stwórz nowe sąsiedztwa

        for i in range(self.ne):
            self.elite_hoods.append(Neighbourhood(self.hive[i], self.radius, self.ttl))

        for i in range(self.nb):
            self.good_hoods.append(Neighbourhood(self.hive[i+self.ne], self.radius, self.ttl))

        # rekrutuj TODO

        self.bee_scouts = self.hive[self.ne+self.nb:]


        # 2. Lokalne poszukiwania
        # TODO zaawansowa kontrola sąsiedztwa (na ten moment pszczoły są blokowane, nie zmienia się radius, etc.)
        for hood in self.elite_hoods:
            while hood.ttl > 0:
                improved = False
                for bee in hood.bees:
                    result = bee.local_search(hood.radius)
                    if result and bee.cost < hood.best_cost:
                        improved = True
                        hood.best_cost = bee.cost
                if not improved:
                    hood.ttl -= 1

        for hood in self.good_hoods:
            while hood.ttl > 0:
                improved = False
                for bee in hood.bees:
                    result = bee.local_search(hood.radius)
                    if result and bee.cost < hood.best_cost:
                        improved = True
                        hood.best_cost = bee.cost
                if not improved:
                    hood.ttl -= 1

        # 3. Zaktualizuj skautów
        for bee in self.bee_scouts:
            bee.global_search()

        # 4. Wróć do ula...
        self.bee_scouts = []
        self.good_hoods = []
        self.elite_hoods = []


'''
Example
'''
random.seed(796)

n = 12
m = 6
sample_case = get_sample_case(4, n, m)
print(sample_case)

Algo = Algorithm(sample_case)

for i in range(1000):
    Algo.step()

print(get_solution(Algo.case, Algo.best_solution))
