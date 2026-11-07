"""Punto de entrada de LogiSmart AI."""
from pathlib import Path
import json
from logismart.scenario import Scenario
from logismart.algorithms.pathfinding import search, multi_stop_route
from logismart.algorithms.local_search import multiple_starts
from logismart.algorithms.game_theory import analyze_game
from logismart.algorithms.minimax import compare
from logismart.visualization import draw_scenario
from logismart.experiments import run_experiments

ROOT = Path(__file__).parent

def main():
    scenario = Scenario.from_json(ROOT / "config" / "escenario.json")
    params = json.loads((ROOT / "config" / "parametros.json").read_text(encoding="utf-8"))
    print("\\n=== LOGISMART AI ===")
    print(f"Escenario: {scenario.name} ({scenario.size}x{scenario.size})")
    print(f"Entregas: {len(scenario.deliveries)} | Obstaculos: {len(scenario.obstacles)}")

    print("\\n--- A. Busqueda heuristica ---")
    for algorithm in ("greedy", "astar"):
        result = search(scenario, scenario.start, scenario.final_destination, algorithm)
        print(algorithm, {k: result[k] for k in ("found","cost","expanded","time_seconds")})
    print("Comparacion de busqueda en tres escenarios:")
    for scenario_file in ("escenario.json", "escenario_2.json", "escenario_3.json"):
        test_scenario = Scenario.from_json(ROOT / "config" / scenario_file)
        metrics = {}
        for algorithm in ("greedy", "astar"):
            r = search(test_scenario, test_scenario.start, test_scenario.final_destination, algorithm)
            metrics[algorithm] = {"found": r["found"], "cost": r["cost"], "expanded": r["expanded"], "time_seconds": r["time_seconds"]}
        print(scenario_file, metrics)
    order = scenario.deliveries
    route = multi_stop_route(scenario, order)
    print("Ruta con entregas en orden configurado:", route["cost"], "Costo encontrado:", route["found"])

    print("\\n--- B. Hill Climbing: diez inicios ---")
    hc = multiple_starts(scenario, params["hill_climbing"]["initial_solutions"],
                         params["hill_climbing"]["max_iterations"], params["seed"])
    print("Mejor costo:", min(x["cost"] for x in hc))

    print("\\n--- C. Metaheuristicas: veinte ejecuciones por metodo ---")
    _, summary = run_experiments(scenario, params, ROOT / "experiments")
    for row in summary: print(row)

    print("\\n--- D. Teoria de juegos ---")
    print(json.dumps(analyze_game(), indent=2, ensure_ascii=False))

    print("\\n--- E. Minimax y poda alfa-beta ---")
    print(compare(params["minimax"]["depth"], scenario.resource_capacity))

    print("\\nResultados CSV guardados en la carpeta experiments.")
    try:
        fig = draw_scenario(scenario, route["path"], "LogiSmart AI - ruta base")
        import matplotlib.pyplot as plt
        plt.show()
    except Exception as exc:
        print("No se pudo mostrar la grafica:", exc)

if __name__ == "__main__":
    main()
