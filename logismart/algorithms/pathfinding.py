"""Greedy Best-First Search y A* sobre la cuadrícula."""
import heapq
import time

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct(parent, current):
    path = [current]
    while current in parent:
        current = parent[current]
        path.append(current)
    return list(reversed(path))

def search(scenario, start, goal, algorithm="astar"):
    if algorithm not in ("astar", "greedy"):
        raise ValueError("algorithm debe ser 'astar' o 'greedy'")
    start_time = time.perf_counter()
    frontier = [(0, 0, start)]
    parent, g = {}, {start: 0}
    expanded, counter = 0, 0
    visited = set()
    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            path = reconstruct(parent, current)
            return {"algorithm": algorithm, "path": path, "cost": g[current],
                    "expanded": expanded, "time_seconds": time.perf_counter()-start_time,
                    "found": True}
        expanded += 1
        for nxt in scenario.neighbors(current):
            tentative = g[current] + scenario.cost(nxt)
            if tentative < g.get(nxt, float("inf")):
                g[nxt] = tentative
                parent[nxt] = current
                h = manhattan(nxt, goal)
                priority = h if algorithm == "greedy" else tentative + h
                counter += 1
                heapq.heappush(frontier, (priority, counter, nxt))
    return {"algorithm": algorithm, "path": [], "cost": float("inf"),
            "expanded": expanded, "time_seconds": time.perf_counter()-start_time,
            "found": False}

def multi_stop_route(scenario, order, algorithm="astar"):
    """Conecta inicio, entregas en el orden indicado y destino final."""
    targets = [scenario.start] + list(order) + [scenario.final_destination]
    full_path, total_cost, expanded, elapsed = [], 0, 0, 0.0
    for a, b in zip(targets, targets[1:]):
        result = search(scenario, a, b, algorithm)
        expanded += result["expanded"]
        elapsed += result["time_seconds"]
        if not result["found"]:
            return {"found": False, "path": [], "cost": float("inf"),
                    "expanded": expanded, "time_seconds": elapsed}
        total_cost += result["cost"]
        full_path.extend(result["path"] if not full_path else result["path"][1:])
    return {"found": True, "path": full_path, "cost": total_cost,
            "expanded": expanded, "time_seconds": elapsed}
