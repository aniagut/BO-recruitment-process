import math
import random
from sample_case import get_sample_case
import string
from enum import Enum
from cost_calculator import calculate_cost
from sample_sol import get_solution

debug = True


def print_debug(*text):
    if debug:
        print(*text)


class TYPES(Enum):
    scout = 0
    forager = 1
    elite_forager = 2


def get_bee_name():
    return "".join(random.sample(string.ascii_letters, 5))


class Bee:
    def __init__(self, case, name, type):
        self.cost = None
        self.position = None
        self.case = case
        self.name = name
        self._type = type
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
    def __init__(self, bees: [Bee], radius, ttl):
        best_bee = min(bees, key=lambda bee: bee.cost)

        self.center: Bee = best_bee
        self.cost = best_bee.cost

        self.bees: [Bee] = bees
        self.radius: int = radius
        self.ttl: int = ttl
        self.max_ttl: int = ttl

    def search(self):
        for bee in self.bees:
            bee.local_search(self.radius)
        found_better = False
        for bee in self.bees:
            if bee.cost < self.cost:
                # znaleziono lepsze rozwiązanie!
                found_better = True
                self.cost = bee.cost
                self.center = bee
                self.ttl = self.max_ttl
        if not found_better:
            self._shrink()

    def _shrink(self):
        self.ttl = max(int(0.8 * self.ttl), 1)
        if self.radius > 1:
            self.radius -= 1


class Algorithm:
    def __init__(self,
                 case: dict,
                 ns: int = 2,
                 ne: int = 1,
                 nre: int = 2,
                 nb: int = 2,
                 nrb: int = 1,
                 ttl: int = 4,
                 radius: int = 10,
                 iterations: int = 100):
        """Inicjalizacja algorytmu pszczelego.

        Parameters:
        case (dict): rozpatrywana instancja problemu
        ns (int): liczba pszczół skautów
        ne (int): liczba elitarnych sąsiedztw
        nre (int): liczba pszczół w każdym elitarnym sąsiedztwie
        nb (int): liczba zwykłych sąsiedztw
        nrb (int): liczba pszczół w każdym zwykłych sąsiedztwie
        ttl (int): czas życia niewydajnego sąsiedztwa
        radius (int): domyślny początkowy promień sąsiedztwa, radius < m
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
        self.iterations = iterations

        self._validate()

        self.best_solution = None
        self.best_score = math.inf

        # Inicjalizacja
        self.hive: [Bee] = []
        self.bee_scouts: [Bee] = []
        self.elite_hoods: [Neighbourhood] = []
        self.good_hoods: [Neighbourhood] = []
        for i in range(ne):
            bees = []
            for j in range(nre):
                name = get_bee_name()
                bees.append(Bee(case, name, TYPES.elite_forager))
            self.elite_hoods.append(Neighbourhood(bees, self.radius, self.ttl))
            self.hive += bees
        for i in range(nb):
            bees = []
            for j in range(nrb):
                name = get_bee_name()
                bees.append(Bee(case, name, TYPES.elite_forager))
            self.good_hoods.append(Neighbourhood(bees, self.radius, self.ttl))
            self.hive += bees
        for i in range(ns):
            name = get_bee_name()
            new_bee = Bee(case, name, TYPES.scout)
            self.bee_scouts.append(new_bee)
            self.hive.append(new_bee)

        print_debug("Pszczoły: " + str([bee.name for bee in self.hive]))

    def _validate(self):
        n = len(self.case['positions'])
        m = len(self.case['candidates'])

        if self.radius >= m:
            raise ValueError("self.radius >= m")

    def step(self):
        """
        PSZCZOŁY WRÓCIŁY DO ULA I DZIELĄ SIĘ SWOIMI WNIOSKAMI.

        SELEKCJA: najgorsze sąsiedztwa są eliminowane, na ich miejsce skauci tworzą nowe sąsiedztwa
        """
        all_neighbourhoods = self.elite_hoods + self.good_hoods + [Neighbourhood([bee], self.radius, self.ttl) for bee in self.bee_scouts]

        best_solution, best_score = all_neighbourhoods[0].center.position, all_neighbourhoods[0].cost
        if best_score < self.best_score:
            print_debug("Nowy najlepszy wynik", all_neighbourhoods[0].cost, 'Znaleziony przez pszczoły:', all_neighbourhoods[0].bees)
            self.best_solution = best_solution
            self.best_score = best_score

        self.elite_hoods = all_neighbourhoods[:self.ne]
        self.good_hoods = all_neighbourhoods[self.ne: (self.ne + self.nb)]
        scout_hoods = [neighbourhood.bees for neighbourhood in all_neighbourhoods[(self.ne + self.nb):]]
        self.bee_scouts = []
        for bees in scout_hoods:
            self.bee_scouts += bees

        for hood in self.elite_hoods:
            if len(hood.bees) > self.nre:
                self.bee_scouts += hood.bees[self.nre:]
                hood.bees = hood.bees[:self.nre]

        for hood in self.good_hoods:
            if len(hood.bees) > self.nrb:
                self.bee_scouts += hood.bees[self.nrb:]
                hood.bees = hood.bees[:self.nrb]

        for hood in self.elite_hoods:
            index = self.nre - len(hood.bees)
            if len(hood.bees) < self.nre:
                hood.bees += self.bee_scouts[:index]
                self.bee_scouts = self.bee_scouts[index:]

        for hood in self.good_hoods:
            index = self.nrb - len(hood.bees)
            if len(hood.bees) < self.nrb:
                hood.bees += self.bee_scouts[:index]
                self.bee_scouts = self.bee_scouts[index:]

        # Pszczoły zostały rozdzielone wedle parametrów
        assert len(self.bee_scouts) == self.ns
        assert len(self.elite_hoods) == self.ne
        assert len(self.good_hoods) == self.nb

        # 1. Lokalne poszukiwania
        for index, hood in enumerate(self.elite_hoods):
            hood.search()
            if hood.ttl < 0:
                # porzuć
                deleted_neighbourhood = self.elite_hoods.pop(index)
                self.bee_scouts += deleted_neighbourhood.bees

        for index, hood in enumerate(self.good_hoods):
            hood.search()
            if hood.ttl < 0:
                # porzuć
                deleted_neighbourhood = self.good_hoods.pop(index)
                self.bee_scouts += deleted_neighbourhood.bees

        # 2. Globalne poszukiwania
        for bee in self.bee_scouts:
            bee.global_search()

        # Całkowita liczba pszczół pozostaje stała
        assert len(self.bee_scouts) + len(self.elite_hoods)*self.nre + len(self.good_hoods)*self.nrb == len(self.hive)

        # 3. Wróć do ula...


'''
Example
'''
random.seed(23+1)

n = 30
m = 10
sample_case = get_sample_case(4, n, m)
print(sample_case)

Algo = Algorithm(sample_case, radius=7)
Algo.step()
print(calculate_cost(Algo.case, Algo.best_solution))
for i in range(66):
    Algo.step()

print(get_solution(Algo.case, Algo.best_solution))
print(calculate_cost(Algo.case, Algo.best_solution))