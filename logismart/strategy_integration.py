
"""Integra las decisiones estratégicas con el escenario logístico."""

from copy import copy
from logismart.algorithms.pathfinding import search


def apply_strategic_decisions(scenario, competitor_strategy, minimax_result):
    """
    Crea una copia del escenario y aplica las consecuencias de:
    1. La estrategia elegida por el competidor.
    2. La asignación de recursos recomendada por Minimax.

    No modifica el escenario original.
    """

    modified = copy(scenario)

    # Copiar las estructuras mutables para proteger el escenario original.
    modified.obstacles = set(scenario.obstacles)
    modified.rough_cells = set(scenario.rough_cells)

    changes = []

    # Consecuencias de la estrategia del competidor.
    if competitor_strategy == "Promocion":
        # La promoción de la competencia aumenta el costo operativo.
        modified.default_cost += 1
        modified.rough_cost += 1

        changes.append(
            "La competencia realizó una promoción. "
            "Se incrementó en una unidad el costo de cada movimiento."
        )

    elif competitor_strategy == "Bloquear recurso":
        # Buscar una ruta inicial para identificar un punto que pueda bloquearse.
        initial_route = search(
            scenario,
            scenario.start,
            scenario.final_destination,
            "astar"
        )

        if initial_route["found"]:
            protected = {
                scenario.start,
                scenario.final_destination,
                *scenario.deliveries
            }

            candidates = [
                cell for cell in initial_route["path"][1:-1]
                if cell not in protected
                and cell not in modified.obstacles
            ]

            if candidates:
                # Se selecciona una celda intermedia de la ruta.
                blocked_cell = candidates[len(candidates) // 2]
                modified.obstacles.add(blocked_cell)

                changes.append(
                    f"La competencia bloqueó el recurso ubicado en "
                    f"{blocked_cell}."
                )
            else:
                changes.append(
                    "No se encontró una celda disponible para bloquear."
                )
        else:
            changes.append(
                "No se pudo bloquear una celda porque no existe una ruta inicial."
            )

    elif competitor_strategy == "No competir":
        changes.append(
            "El competidor decidió no intervenir en la operación."
        )

    else:
        raise ValueError("Estrategia del competidor no reconocida.")

    # Consecuencia de la decisión de asignación de recursos de Minimax.
    allocated = int(minimax_result.get("best_action", 0))
    remaining = max(
        0,
        scenario.resource_capacity - allocated
    )

    modified.resource_capacity = remaining

    # Cada unidad asignada consume dos unidades del presupuesto.
    modified.initial_budget = max(
        0,
        scenario.initial_budget - (allocated * 2)
    )

    changes.append(
        f"Minimax asignó {allocated} unidades de recurso. "
        f"Quedan {remaining} unidades disponibles."
    )

    changes.append(
        f"Presupuesto restante: {modified.initial_budget}."
    )

    return {
        "scenario": modified,
        "changes": changes,
        "allocated_resources": allocated,
        "remaining_resources": remaining,
        "remaining_budget": modified.initial_budget,
        "competitor_strategy": competitor_strategy
    }
