"""Recocido simulado y algoritmo genetico para ordenar las entregas."""
import math, random, time
from .pathfinding import multi_stop_route

_OBJECTIVE_CACHE = {}
def objective(scenario, order):
    key = (id(scenario), tuple(order))
    if key not in _OBJECTIVE_CACHE:
        _OBJECTIVE_CACHE[key] = multi_stop_route(scenario, order)["cost"]
    return _OBJECTIVE_CACHE[key]

def simulated_annealing(scenario, seed=42, initial_temperature=100.0,
                         cooling_rate=0.995, minimum_temperature=0.01):
    rng = random.Random(seed)
    current = scenario.deliveries.copy()
    rng.shuffle(current)
    current_cost = objective(scenario, current)
    best, best_cost = current.copy(), current_cost
    temperature, evaluations = initial_temperature, 1
    start = time.perf_counter()
    while temperature > minimum_temperature:
        candidate = current.copy()
        if len(candidate) >= 2:
            i, j = rng.sample(range(len(candidate)), 2)
            candidate[i], candidate[j] = candidate[j], candidate[i]
        candidate_cost = objective(scenario, candidate)
        evaluations += 1
        delta = candidate_cost - current_cost
        if delta < 0 or rng.random() < math.exp(-delta / temperature):
            current, current_cost = candidate, candidate_cost
        if current_cost < best_cost:
            best, best_cost = current.copy(), current_cost
        temperature *= cooling_rate
    return {"best_order": best, "best_cost": best_cost, "evaluations": evaluations,
            "time_seconds": time.perf_counter()-start}

def genetic_algorithm(scenario, seed=42, population_size=40, generations=150,
                      crossover_rate=0.85, mutation_rate=0.15, tournament_size=3):
    rng = random.Random(seed)
    base = scenario.deliveries.copy()
    def make_individual():
        x = base.copy(); rng.shuffle(x); return x
    def fitness(x): return objective(scenario, x)
    def select(pop):
        contestants = rng.sample(pop, min(tournament_size, len(pop)))
        return min(contestants, key=fitness).copy()
    def crossover(a, b):
        if len(a) < 2 or rng.random() >= crossover_rate: return a.copy()
        lo, hi = sorted(rng.sample(range(len(a)), 2))
        child = [None] * len(a)
        child[lo:hi+1] = a[lo:hi+1]
        fill = [gene for gene in b if gene not in child]
        k = 0
        for i in range(len(child)):
            if child[i] is None:
                child[i] = fill[k]; k += 1
        return child
    def mutate(x):
        x = x.copy()
        if len(x) >= 2 and rng.random() < mutation_rate:
            i, j = rng.sample(range(len(x)), 2); x[i], x[j] = x[j], x[i]
        return x
    start = time.perf_counter()
    population = [make_individual() for _ in range(population_size)]
    evaluations = len(population)
    best = min(population, key=fitness).copy()
    best_cost = fitness(best)
    for _ in range(generations):
        new_population = [best.copy()]  # elitismo
        while len(new_population) < population_size:
            p1, p2 = select(population), select(population)
            child = mutate(crossover(p1, p2))
            new_population.append(child)
        population = new_population
        evaluations += len(population)-1
        candidate = min(population, key=fitness)
        candidate_cost = fitness(candidate)
        if candidate_cost < best_cost:
            best, best_cost = candidate.copy(), candidate_cost
    return {"best_order": best, "best_cost": best_cost, "evaluations": evaluations,
            "time_seconds": time.perf_counter()-start}
