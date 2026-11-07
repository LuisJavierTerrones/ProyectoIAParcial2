"""Juego estatico de dos jugadores con tres estrategias cada uno."""
import numpy as np

# Filas: Empresa (conservadora, equilibrada, agresiva).
# Columnas: Competidor (no competir, promocion, bloquear recurso).
PAYOFF_A = np.array([[4, 2, 1], [5, 3, 0], [2, 4, -2]], dtype=float)
PAYOFF_B = np.array([[3, 2, 1], [2, 3, 4], [1, 5, 2]], dtype=float)
STRATEGIES_A = ["Conservadora", "Equilibrada", "Agresiva"]
STRATEGIES_B = ["No competir", "Promocion", "Bloquear recurso"]

def analyze_game():
    best_a = [set(np.where(PAYOFF_A[:, j] == PAYOFF_A[:, j].max())[0]) for j in range(3)]
    best_b = [set(np.where(PAYOFF_B[i, :] == PAYOFF_B[i, :].max())[0]) for i in range(3)]
    nash = []
    for i in range(3):
        for j in range(3):
            if i in best_a[j] and j in best_b[i]:
                nash.append((STRATEGIES_A[i], STRATEGIES_B[j], PAYOFF_A[i,j], PAYOFF_B[i,j]))
    dominant_a = [i for i in range(3) if all(i in s for s in best_a)]
    dominant_b = [j for j in range(3) if all(j in s for s in best_b)]
    return {"payoff_a": PAYOFF_A.tolist(), "payoff_b": PAYOFF_B.tolist(),
            "best_responses_a": [[STRATEGIES_A[i] for i in sorted(s)] for s in best_a],
            "best_responses_b": [[STRATEGIES_B[j] for j in sorted(s)] for s in best_b],
            "nash_pure": nash,
            "dominant_a": [STRATEGIES_A[i] for i in dominant_a],
            "dominant_b": [STRATEGIES_B[j] for j in dominant_b]}
