"""Experimentos reproducibles y exportacion de resultados."""
from pathlib import Path
import csv, statistics
from .algorithms.local_search import multiple_starts
from .algorithms.metaheuristics import simulated_annealing, genetic_algorithm

def run_experiments(scenario, params, output_dir="experiments"):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    seed = params["seed"]
    hc = multiple_starts(scenario, params["hill_climbing"]["initial_solutions"],
                         params["hill_climbing"]["max_iterations"], seed)
    rows = []
    for i, result in enumerate(hc):
        rows.append({"method":"Hill Climbing", "run":i+1, "cost":result["cost"],
                     "evaluations":result["evaluations"], "time_seconds":result["time_seconds"]})
    sa_cfg = params["simulated_annealing"]
    sa_results = [simulated_annealing(scenario, seed+i, sa_cfg["initial_temperature"],
                    sa_cfg["cooling_rate"], sa_cfg["minimum_temperature"]) for i in range(sa_cfg["runs"])]
    for i, r in enumerate(sa_results):
        rows.append({"method":"Recocido simulado", "run":i+1, "cost":r["best_cost"],
                     "evaluations":r["evaluations"], "time_seconds":r["time_seconds"]})
    ga_cfg = params["genetic_algorithm"]
    ga_results = [genetic_algorithm(scenario, seed+i, ga_cfg["population_size"],
                    ga_cfg["generations"], ga_cfg["crossover_rate"], ga_cfg["mutation_rate"],
                    ga_cfg["tournament_size"]) for i in range(ga_cfg["runs"])]
    for i, r in enumerate(ga_results):
        rows.append({"method":"Algoritmo genetico", "run":i+1, "cost":r["best_cost"],
                     "evaluations":r["evaluations"], "time_seconds":r["time_seconds"]})
    csv_path = out / "resultados.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["method","run","cost","evaluations","time_seconds"])
        writer.writeheader(); writer.writerows(rows)
    summary = []
    for method in sorted({r["method"] for r in rows}):
        vals = [float(r["cost"]) for r in rows if r["method"] == method]
        times = [float(r["time_seconds"]) for r in rows if r["method"] == method and r["time_seconds"] != ""]
        evals = [float(r["evaluations"]) for r in rows if r["method"] == method]
        summary.append({"method":method, "best":min(vals), "average":statistics.mean(vals),
                        "stdev":statistics.stdev(vals) if len(vals)>1 else 0,
                        "average_evaluations":statistics.mean(evals),
                        "average_time_seconds":statistics.mean(times) if times else None})
    with (out / "resumen.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader(); writer.writerows(summary)
    return rows, summary
