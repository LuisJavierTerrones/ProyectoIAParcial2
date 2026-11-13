"""Interfaz gráfica de LogiSmart AI construida sobre los módulos originales."""
from pathlib import Path
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logismart.scenario import Scenario
from logismart.algorithms.pathfinding import search, multi_stop_route
from logismart.algorithms.local_search import multiple_starts
from logismart.algorithms.metaheuristics import simulated_annealing, genetic_algorithm
from logismart.algorithms.game_theory import analyze_game, STRATEGIES_A, STRATEGIES_B
from logismart.algorithms.minimax import compare
from logismart.strategy_integration import apply_strategic_decisions
from logismart.experiments import run_experiments

st.set_page_config(page_title="LogiSmart AI", page_icon="🚚", layout="wide")

# Estilo de aplicación para una presentación limpia en pantalla.
st.markdown("""
<style>
  .stApp {background: #0b1220; color: #e5edf7;}
  [data-testid="stSidebar"] {background: #111c2e;}
  [data-testid="stMetric"] {background: #142238; border: 1px solid #263b57; padding: 13px; border-radius: 12px;}
  .hero {padding: 18px 22px; border: 1px solid #263b57; border-radius: 16px; background: linear-gradient(120deg,#14263e,#101827); margin-bottom: 14px;}
  .hero h1 {margin:0; color:#f4f8ff; font-size:2rem;}
  .hero p {color:#a9bdd5; margin:6px 0 0 0;}
  div[data-testid="stTabs"] button {font-weight:600;}
  .small-note {color:#9fb1c8; font-size:0.88rem;}
</style>
""", unsafe_allow_html=True)

CONFIG = ROOT / "config"
PARAMS = json.loads((CONFIG / "parametros.json").read_text(encoding="utf-8"))
SCENARIOS = {
    "Escenario base": "escenario.json",
    "Escenario 2": "escenario_2.json",
    "Escenario 3": "escenario_3.json",
}


def load_scenario(label):
    return Scenario.from_json(CONFIG / SCENARIOS[label])


def draw_map(scenario, path=None, title="Mapa logístico"):
    """Dibuja el mapa usando las coordenadas y costos del objeto Scenario real."""
    n = scenario.size
    grid = [[0 for _ in range(n)] for _ in range(n)]
    for r, c in scenario.rough_cells:
        grid[r][c] = 1
    for r, c in scenario.obstacles:
        grid[r][c] = 2
    fig, ax = plt.subplots(figsize=(7.2, 6.0), facecolor="#0f1726")
    ax.set_facecolor("#142238")
    cmap = ListedColormap(["#243b55", "#a66a2c", "#263142"])
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=2)
    ax.set_xticks(range(n)); ax.set_yticks(range(n))
    ax.set_xticklabels(range(n), color="#cbd5e1", fontsize=8)
    ax.set_yticklabels(range(n), color="#cbd5e1", fontsize=8)
    ax.set_xticks([x-.5 for x in range(1,n)], minor=True)
    ax.set_yticks([y-.5 for y in range(1,n)], minor=True)
    ax.grid(which="minor", color="#8294aa", alpha=.23, linewidth=.6)
    ax.tick_params(length=0)
    if path:
        ax.plot([p[1] for p in path], [p[0] for p in path], color="#45d6c5", linewidth=3, alpha=.95, zorder=4)
    # Marcas de almacén, entregas y destino.
    ax.scatter(scenario.start[1], scenario.start[0], marker="s", s=190, c="#34d399", edgecolors="white", linewidths=1.2, zorder=6, label="Almacén")
    for i, (r,c) in enumerate(scenario.deliveries, 1):
        ax.scatter(c, r, marker="o", s=150, c="#60a5fa", edgecolors="white", linewidths=1, zorder=6)
        ax.text(c, r, str(i), color="#07111f", weight="bold", ha="center", va="center", fontsize=9, zorder=7)
    ax.scatter(scenario.final_destination[1], scenario.final_destination[0], marker="*", s=260, c="#fb7185", edgecolors="white", linewidths=.8, zorder=6, label="Destino")
    ax.set_title(title, color="#f1f5f9", fontsize=13, pad=12, weight="bold")
    ax.legend(loc="upper center", bbox_to_anchor=(.5,-.08), ncol=2, frameon=False, labelcolor="#dbeafe")
    for spine in ax.spines.values(): spine.set_color("#34465f")
    fig.tight_layout()
    return fig


st.markdown("""
<div class="hero">
  <h1>🚚 LogiSmart AI</h1>
  <p>Centro de control inteligente · planificación de rutas · optimización · decisiones estratégicas</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    scenario_label = st.selectbox("Escenario logístico", list(SCENARIOS.keys()))
    selected_algorithm = st.selectbox("Algoritmo de ruta", ["A*", "Greedy"])
    st.caption("Los cálculos se realizan con los módulos Python del proyecto.")
    st.divider()
    st.markdown("### Leyenda del mapa")
    st.markdown("🟩 Almacén  ·  🔵 Entregas  ·  🌟 Destino")
    st.markdown("🟧 Terreno difícil  ·  ⬛ Obstáculo  ·  🟦 Ruta")

scenario = load_scenario(scenario_label)
algorithm_key = "astar" if selected_algorithm == "A*" else "greedy"
route_result = search(scenario, scenario.start, scenario.final_destination, algorithm_key)

# Resumen superior de ejecución real.
c1,c2,c3,c4 = st.columns(4)
c1.metric("Dimensión", f"{scenario.size} × {scenario.size}")
c2.metric("Entregas", len(scenario.deliveries))
c3.metric("Costo de ruta directa", route_result["cost"] if route_result["found"] else "Sin ruta")
c4.metric("Nodos expandidos", route_result["expanded"])

route_tab, opt_tab, game_tab, report_tab = st.tabs([
    "🗺️ Mapa y rutas", "🧬 Optimización", "♟️ Estrategia", "📊 Experimentos"
])

with route_tab:
    left, right = st.columns([1.25, 1])
    with left:
        st.pyplot(draw_map(scenario, route_result["path"], f"{scenario_label} · {selected_algorithm}"), use_container_width=True)
    with right:
        st.subheader("Resultado de búsqueda")
        st.success("Ruta encontrada" if route_result["found"] else "No existe una ruta")
        m1,m2 = st.columns(2)
        m1.metric("Costo", route_result["cost"] if route_result["found"] else "—")
        m2.metric("Tiempo", f"{route_result['time_seconds']*1000:.3f} ms")
        st.write(f"**Algoritmo:** {selected_algorithm}")
        st.write(f"**Inicio:** {scenario.start}")
        st.write(f"**Destino:** {scenario.final_destination}")
        st.write(f"**Longitud de ruta:** {len(route_result['path'])} celdas")
        with st.expander("Ver coordenadas de la ruta"):
            st.write(route_result["path"])
    st.divider()
    st.subheader("Comparación Greedy vs A*")
    if st.button("Ejecutar comparación en los tres escenarios", key="compare_paths"):
        rows=[]
        for label, filename in SCENARIOS.items():
            sc=Scenario.from_json(CONFIG/filename)
            for alg in ("greedy","astar"):
                r=search(sc,sc.start,sc.final_destination,alg)
                rows.append({"Escenario":label,"Algoritmo":alg.upper(),"Encontró ruta":r["found"],"Costo":r["cost"],"Nodos":r["expanded"],"Tiempo (ms)":r["time_seconds"]*1000})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with opt_tab:
    st.subheader("Optimización del orden de entregas")
    st.write("Cada solución representa un orden de visita. Los algoritmos llaman a las implementaciones originales del proyecto.")
    st.caption("El costo base de la secuencia configurada es calculado en tiempo real.")
    base_route=multi_stop_route(scenario,scenario.deliveries)
    st.metric("Costo del orden configurado", base_route["cost"] if base_route["found"] else "Sin ruta")
    run_choice=st.radio("Método a ejecutar", ["Hill Climbing (10 inicios)","Recocido simulado (20 ejecuciones)","Algoritmo genético (20 ejecuciones)","Comparar los tres métodos"], horizontal=False)
    if st.button("▶ Ejecutar optimización", type="primary", key="run_optimizer"):
        with st.spinner("Ejecutando algoritmo real y calculando métricas..."):
            if run_choice == "Hill Climbing (10 inicios)":
                cfg=PARAMS["hill_climbing"]
                rs=multiple_starts(scenario,cfg["initial_solutions"],cfg["max_iterations"],PARAMS["seed"])
                rows=[{"Ejecución":i+1,"Costo":x["cost"],"Evaluaciones":x["evaluations"],"Tiempo (ms)":x["time_seconds"]*1000,"Orden":str(x["order"])} for i,x in enumerate(rs)]
                st.session_state["optimizer_rows"]=pd.DataFrame(rows)
                st.session_state["optimizer_title"]="Hill Climbing"
            else:
                rows=[]
                seed=PARAMS["seed"]
                if run_choice in ("Recocido simulado (20 ejecuciones)", "Comparar los tres métodos"):
                    cfg=PARAMS["simulated_annealing"]
                    sa_results=[simulated_annealing(scenario,seed+i,cfg["initial_temperature"],cfg["cooling_rate"],cfg["minimum_temperature"]) for i in range(cfg["runs"])]
                    rows.extend({"method":"Recocido simulado","run":i+1,"cost":r["best_cost"],"evaluations":r["evaluations"],"time_seconds":r["time_seconds"]} for i,r in enumerate(sa_results))
                if run_choice in ("Algoritmo genético (20 ejecuciones)", "Comparar los tres métodos"):
                    cfg=PARAMS["genetic_algorithm"]
                    ga_results=[genetic_algorithm(scenario,seed+i,cfg["population_size"],cfg["generations"],cfg["crossover_rate"],cfg["mutation_rate"],cfg["tournament_size"]) for i in range(cfg["runs"])]
                    rows.extend({"method":"Algoritmo genetico","run":i+1,"cost":r["best_cost"],"evaluations":r["evaluations"],"time_seconds":r["time_seconds"]} for i,r in enumerate(ga_results))
                if run_choice == "Comparar los tres métodos":
                    cfg=PARAMS["hill_climbing"]
                    hc_results=multiple_starts(scenario,cfg["initial_solutions"],cfg["max_iterations"],seed)
                    rows.extend({"method":"Hill Climbing","run":i+1,"cost":r["cost"],"evaluations":r["evaluations"],"time_seconds":r["time_seconds"]} for i,r in enumerate(hc_results))
                    title="Comparación de los tres métodos"
                elif run_choice == "Recocido simulado (20 ejecuciones)":
                    title="Recocido simulado"
                else:
                    title="Algoritmo genético"
                st.session_state["optimizer_rows"]=pd.DataFrame(rows)
                st.session_state["optimizer_title"]=title
    if "optimizer_rows" in st.session_state:
        df=st.session_state["optimizer_rows"]
        st.markdown(f"### {st.session_state['optimizer_title']}")
        st.dataframe(df,use_container_width=True,hide_index=True)
        cost_col="cost" if "cost" in df.columns else "Costo"
        eval_col="evaluations" if "evaluations" in df.columns else "Evaluaciones"
        if cost_col in df.columns:
            a,b=st.columns(2)
            a.metric("Mejor costo",f"{df[cost_col].min():.2f}")
            b.metric("Promedio de evaluaciones",f"{df[eval_col].mean():,.1f}")
            st.bar_chart(df.set_index(df.columns[0])[[cost_col,eval_col]] if len(df)<30 else df[[cost_col,eval_col]])


with game_tab:
    st.subheader("Teoría de juegos")

    game = analyze_game()

    a, b = st.columns(2)

    with a:
        st.markdown("**Matriz de pagos · Empresa**")
        st.dataframe(
            pd.DataFrame(
                game["payoff_a"],
                index=STRATEGIES_A,
                columns=STRATEGIES_B
            ),
            use_container_width=True
        )

    with b:
        st.markdown("**Matriz de pagos · Competidor**")
        st.dataframe(
            pd.DataFrame(
                game["payoff_b"],
                index=STRATEGIES_A,
                columns=STRATEGIES_B
            ),
            use_container_width=True
        )

    if game["nash_pure"]:
        for n in game["nash_pure"]:
            st.success(
                f"Equilibrio de Nash: {n[0]} / {n[1]} "
                f"· Pagos ({n[2]:g}, {n[3]:g})"
            )
    else:
        st.info("No se encontró equilibrio puro.")

    st.write("**Estrategias dominantes de la empresa:**",
             game["dominant_a"] or "No hay")

    st.write("**Estrategias dominantes del competidor:**",
             game["dominant_b"] or "No hay")

    st.caption(
        "Los pagos representan supuestos didácticos del modelo."
    )

    st.divider()

    st.subheader("Minimax vs poda alfa-beta")

    depth = st.slider(
        "Profundidad de búsqueda",
        min_value=1,
        max_value=8,
        value=PARAMS["minimax"]["depth"]
    )

    if st.button("Calcular árbol adversario", key="run_minimax"):
        result = compare(depth, scenario.resource_capacity)

        x, y, z = st.columns(3)

        x.metric("Valor Minimax", result["minimax_value"])
        y.metric("Nodos Minimax", result["minimax_nodes"])
        z.metric("Nodos alfa-beta", result["alphabeta_nodes"])

        m1, m2, m3 = st.columns(3)

        m1.metric("Ramas podadas", result["pruned"])
        m2.metric("Unidades asignadas", result["best_action"])
        m3.metric("Unidades restantes", result["remaining_units"])

        st.session_state["minimax_result"] = result

        if result["same_value"]:
            st.success("Minimax y alfa-beta obtuvieron el mismo valor.")
        else:
            st.error("Los resultados no coinciden.")

    st.divider()

    st.subheader("Integración de decisiones estratégicas")

    st.write(
        "Selecciona la estrategia del competidor. "
        "El sistema aplicará sus consecuencias al escenario "
        "y volverá a calcular la ruta con A*."
    )

    default_strategy = (
        game["nash_pure"][0][1]
        if game["nash_pure"]
        else STRATEGIES_B[0]
    )

    strategy_options = STRATEGIES_B

    selected_strategy = st.selectbox(
        "Estrategia del competidor",
        strategy_options,
        index=strategy_options.index(default_strategy)
    )

    if st.button(
        "Aplicar decisiones y recalcular ruta",
        type="primary",
        key="apply_strategies"
    ):

        # Calcular Minimax con los recursos del escenario actual.
        minimax_result = compare(
            depth,
            scenario.resource_capacity
        )

        # Aplicar las consecuencias de las dos decisiones.
        integration = apply_strategic_decisions(
            scenario,
            selected_strategy,
            minimax_result
        )

        modified_scenario = integration["scenario"]

        # Calcular ruta original y ruta modificada.
        original_route = search(
            scenario,
            scenario.start,
            scenario.final_destination,
            "astar"
        )

        modified_route = search(
            modified_scenario,
            modified_scenario.start,
            modified_scenario.final_destination,
            "astar"
        )

        st.session_state["integration_result"] = {
            "integration": integration,
            "original_route": original_route,
            "modified_route": modified_route,
            "modified_scenario": modified_scenario
        }

    if "integration_result" in st.session_state:

        data = st.session_state["integration_result"]

        integration = data["integration"]
        original_route = data["original_route"]
        modified_route = data["modified_route"]
        modified_scenario = data["modified_scenario"]

        st.markdown("### Consecuencias de las decisiones")

        for change in integration["changes"]:
            st.write("•", change)

        st.markdown("### Comparación de rutas")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Escenario original**")

            st.metric(
                "Costo de ruta",
                original_route["cost"]
                if original_route["found"]
                else "Sin ruta"
            )

            st.pyplot(
                draw_map(
                    scenario,
                    original_route["path"],
                    "Ruta original"
                ),
                use_container_width=True
            )

        with col2:
            st.markdown("**Escenario con decisiones aplicadas**")

            st.metric(
                "Costo de ruta",
                modified_route["cost"]
                if modified_route["found"]
                else "Sin ruta"
            )

            st.pyplot(
                draw_map(
                    modified_scenario,
                    modified_route["path"],
                    "Ruta modificada"
                ),
                use_container_width=True
            )

        st.markdown("### Recursos después de la decisión")

        r1, r2, r3 = st.columns(3)

        r1.metric(
            "Recursos disponibles",
            integration["remaining_resources"]
        )

        r2.metric(
            "Presupuesto restante",
            integration["remaining_budget"]
        )

        r3.metric(
            "Unidades asignadas",
            integration["allocated_resources"]
        )

        if original_route["found"] and modified_route["found"]:
            difference = (
                modified_route["cost"] - original_route["cost"]
            )

            st.metric(
                "Variación del costo de ruta",
                f"{difference:+g}"
            )

        elif not modified_route["found"]:
            st.warning(
                "Las decisiones aplicadas impidieron encontrar "
                "una ruta hacia el destino."
            )


with report_tab:
    st.subheader("Centro de experimentación")
    st.write("Ejecuta la batería completa con la semilla y los parámetros documentados.")
    if st.button("▶ Ejecutar batería experimental completa",type="primary",key="run_full_experiments"):
        with st.spinner("Ejecutando 10 inicios de Hill Climbing y 20 ejecuciones por metaheurística..."):
            rows,summary=run_experiments(scenario,PARAMS,ROOT/"experiments")
        st.session_state["full_summary"]=pd.DataFrame(summary)
        st.session_state["full_rows"]=pd.DataFrame(rows)
    if "full_summary" in st.session_state:
        st.markdown("### Resumen estadístico")
        st.dataframe(st.session_state["full_summary"],use_container_width=True,hide_index=True)
        st.bar_chart(st.session_state["full_summary"].set_index("method")[["best","average"]])
        st.markdown("### Ejecuciones individuales")
        st.dataframe(st.session_state["full_rows"],use_container_width=True,hide_index=True)
        st.download_button("Descargar resultados.csv",st.session_state["full_rows"].to_csv(index=False).encode("utf-8"),"resultados.csv","text/csv")
        st.download_button("Descargar resumen.csv",st.session_state["full_summary"].to_csv(index=False).encode("utf-8"),"resumen.csv","text/csv")
    else:
        csv_path=ROOT/"experiments"/"resumen.csv"
        if csv_path.exists():
            st.caption("Último resumen guardado en el proyecto")
            st.dataframe(pd.read_csv(csv_path),use_container_width=True,hide_index=True)

st.divider()
st.markdown("<p class='small-note'>LogiSmart AI · Interfaz gráfica sobre las implementaciones originales en Python. Los módulos estratégicos se presentan como análisis; sus decisiones aún no modifican automáticamente el mapa o los costos de ruta.</p>",unsafe_allow_html=True)
