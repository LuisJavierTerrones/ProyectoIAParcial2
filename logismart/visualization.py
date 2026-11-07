"""Visualizacion del escenario y una ruta."""
import matplotlib.pyplot as plt

def draw_scenario(scenario, path=None, title="Escenario logistico"):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-0.5, scenario.size-0.5); ax.set_ylim(scenario.size-0.5, -0.5)
    ax.set_xticks(range(scenario.size)); ax.set_yticks(range(scenario.size))
    ax.grid(True, alpha=0.35)
    for r, c in scenario.obstacles:
        ax.scatter(c, r, marker="s", s=180, color="black")
    for r, c in scenario.rough_cells:
        if (r,c) not in scenario.obstacles:
            ax.scatter(c, r, marker="s", s=150, color="orange", alpha=0.55)
    ax.scatter(scenario.start[1], scenario.start[0], marker="s", s=230, color="green", label="Almacen")
    ax.scatter(scenario.final_destination[1], scenario.final_destination[0], marker="*", s=280, color="red", label="Destino final")
    for i, (r,c) in enumerate(scenario.deliveries, 1):
        ax.scatter(c, r, marker="o", s=180, color="royalblue")
        ax.text(c, r, str(i), color="white", ha="center", va="center", weight="bold")
    if path:
        ax.plot([p[1] for p in path], [p[0] for p in path], color="purple", linewidth=2.5, label="Ruta")
    ax.set_title(title); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    fig.tight_layout()
    return fig
