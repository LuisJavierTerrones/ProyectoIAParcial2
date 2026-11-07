"""Hill Climbing con vecindad de intercambio de dos entregas."""
import random
import time
from .pathfinding import multi_stop_route

def route_cost(scenario, order):
    return multi_stop_route(scenario, order)["cost"]

def hill_climbing(scenario, initial_order=None, max_iterations=500, seed=42):
    rng = random.Random(seed)
    current = list(initial_order if initial_order is not None else scenario.deliveries)
    if initial_order is None:
        rng.shuffle(current)
    start_time = time.perf_counter()
    evaluations = 1
    current_cost = route_cost(scenario, current)
    iterations = 0
    while iterations < max_iterations:
        best, best_cost = current, current_cost
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                candidate = current.copy()
                candidate[i], candidate[j] = candidate[j], candidate[i]
                cost = route_cost(scenario, candidate)
                evaluations += 1
                if cost < best_cost:
                    best, best_cost = candidate, cost
        if best_cost >= current_cost:
            break
        current, current_cost = best, best_cost
        iterations += 1
    return {"order": current, "cost": current_cost, "iterations": iterations,
            "evaluations": evaluations, "time_seconds": time.perf_counter()-start_time}

def multiple_starts(scenario, count=10, max_iterations=500, seed=42):
    if count < 1:
        raise ValueError("count debe ser al menos 1")
    rng = random.Random(seed)
    results = []
    for i in range(count):
        order = scenario.deliveries.copy()
        rng.shuffle(order)
        results.append(hill_climbing(scenario, order, max_iterations, seed+i))
    return results
