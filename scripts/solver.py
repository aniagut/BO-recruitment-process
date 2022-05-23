import math
import random
from sample_case import get_sample_case
import string
from enum import Enum

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
        self.ttl -= 1
        if self.radius > 1:
            self.radius -= 1

class GlobalNeighbourhood(Neighbourhood):
    '''
    Abstrakcyjne sąsiedztwo przypisywane skautom
    '''

    def __init__(self, bee):
        super().__init__([bee], math.inf, math.inf)

    def search(self):
        pass

class Algorithm:
    def __init__(self,
                 case: dict,
                 ns: int = 2,
                 ne: int = 1,
                 nre: int = 2,
                 nb: int = 2,
                 nrb: int = 1,
                 ttl: int = 5,
                 radius: int = 2,
                 shrink_factor: int = 1,
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
        self.bee_scouts: [Neighbourhood] = []
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
            global_neighbourhood = GlobalNeighbourhood(new_bee)
            self.bee_scouts.append(global_neighbourhood)
            self.hive.append(new_bee)

        print_debug("Pszczoły:" + str([bee.name for bee in self.hive]))

    def _validate(self):
        n = len(self.case['positions'])
        m = len(self.case['candidates'])

        if self.radius >= m:
            raise ValueError("self.radius >= m")

    def step(self):
        """
        PSZCZOŁY WRÓCIŁY DO ULA I DZIELĄ SIĘ SWOIMI WNIOSKAMI.

        SELEKCJA: najgorsze sąsiedztwa są eliminowane

        ne najlepszych pszczół tworzy elitarne sąsiedztwa
        nb kolejnych pszczół tworzy nieelitarne sąsiedztwa
        pszczoły rekrutują pomocników i razem z nimi wylatują w przydzielone miejsca

        reszta pszczół zostaje skautami i przeszukuje globalną przestrzeń rozwiązań
        """
        neighbourhoods_evaluated = [Neighbourhood([Bee(self.case, 'TEST', 'TEST')], self.radius, self.ttl)]

        best_solution, best_score = neighbourhoods_evaluated[0].center.position, neighbourhoods_evaluated[0].cost
        if best_score < self.best_score:
            print_debug("Nowy najlepszy wynik", neighbourhoods_evaluated[0].cost)
            self.best_solution = best_solution
            self.best_score = best_score


        # eliminuj i rekrutuj TODO


        # 2. Lokalne poszukiwania
        # TODO zaawansowa kontrola sąsiedztwa (na ten moment pszczoły są blokowane, nie zmienia się radius, etc.)
        for hood in self.elite_hoods:
            hood.search()
            if hood.ttl < 0:
                pass #abandon

        for hood in self.good_hoods:
            hood.search()
            if hood.ttl < 0:
                pass #abandon

        # 3. Zaktualizuj skautów
        for hood in self.bee_scouts:
            hood.search()

        # 4. Wróć do ula...

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
