#  LogiSmart AI
### Sistema inteligente de planificación, optimización y toma de decisiones adversarias

**Proyecto académico – Segundo parcial**  
**Lenguaje:** Python  
**Repositorio:** [ProyectoIAParcial2](https://github.com/LuisJavierTerrones/ProyectoIAParcial2)

---

## 1. Descripción del proyecto

LogiSmart AI es un sistema inteligente desarrollado en Python para resolver un problema de planificación logística mediante técnicas de inteligencia artificial y algoritmos de búsqueda y optimización.

El sistema representa una red logística mediante una cuadrícula de 12 × 12, donde se modelan almacenes, destinos, puntos de entrega, obstáculos, terrenos con costos variables y restricciones de recursos.

Su propósito es comparar diferentes estrategias algorítmicas para encontrar rutas, optimizar el orden de las entregas y analizar decisiones estratégicas entre agentes competidores.

## 2. Objetivos

- Encontrar rutas eficientes mediante algoritmos de búsqueda heurística.
- Optimizar el orden de visita de múltiples puntos de entrega.
- Comparar técnicas de búsqueda local y metaheurísticas.
- Analizar situaciones competitivas mediante teoría de juegos.
- Resolver problemas de decisión adversaria mediante Minimax y poda alfa-beta.
- Evaluar el rendimiento de los algoritmos mediante experimentos reproducibles.

## 3. Tecnologías utilizadas

| Tecnología | Aplicación |
|---|---|
| Python | Lenguaje principal |
| NumPy | Operaciones y procesamiento numérico |
| Pandas | Gestión de resultados experimentales |
| Matplotlib | Visualización de mapas y gráficas |
| NetworkX | Herramientas de representación de redes |
| Streamlit | Interfaz gráfica interactiva |
| JSON | Configuración de escenarios y parámetros |
| CSV | Almacenamiento de resultados |

## 4. Módulos del sistema

### A. Búsqueda heurística
Implementa:
- Greedy Best-First Search.
- A*.

Compara costos, nodos expandidos, tiempos de ejecución y rutas encontradas.

### B. Búsqueda local
Implementa Hill Climbing para optimizar el orden de visita de las entregas mediante múltiples soluciones iniciales.

### C. Metaheurísticas
Incluye:
- Recocido simulado (Simulated Annealing).
- Algoritmo genético (Genetic Algorithm).

Se realizan 20 ejecuciones por método, registrando métricas para comparar su rendimiento.

### D. Teoría de juegos
Modela decisiones estratégicas entre dos jugadores mediante una matriz de pagos. Analiza mejores respuestas, estrategias dominantes y equilibrios de Nash.

### E. Búsqueda adversaria
Implementa:
- Minimax.
- Minimax con poda alfa-beta.

Compara valores de utilidad y cantidad de nodos evaluados.

## 5. Arquitectura del proyecto

```text
LogiSmart_AI/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── INFORME_TECNICO.md
├── INFORME_TECNICO_PLANTILLA.md
├── INICIAR_LOGISMART.bat
│
├── config/
│   ├── escenario.json
│   ├── escenario_2.json
│   ├── escenario_3.json
│   └── parametros.json
│
├── logismart/
│   ├── __init__.py
│   ├── scenario.py
│   ├── experiments.py
│   ├── strategy_integration.py
│   ├── visualization.py
│   │
│   └── algorithms/
│       ├── __init__.py
│       ├── pathfinding.py
│       ├── local_search.py
│       ├── metaheuristics.py
│       ├── game_theory.py
│       └── minimax.py
│
├── experiments/
│   ├── resultados.csv
│   ├── resumen.csv
│   └── comparacion_evaluaciones.png
│
└── tests/
    └── test_logismart.py
```

## 6. Instalación

### Requisitos previos

- Windows 10 o superior.
- Python 3.10 o superior.
- Git.
- Conexión a Internet para instalar las dependencias.

### Clonar el repositorio

Abrir CMD y ejecutar:

```cmd
git clone https://github.com/LuisJavierTerrones/ProyectoIAParcial2.git
```

Entrar en la carpeta:

```cmd
cd ProyectoIAParcial2
```

### Crear entorno virtual

```cmd
py -m venv .venv
```

### Instalar dependencias

```cmd
.venv\Scripts\python.exe -m pip install --upgrade pip
```

```cmd
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 7. Ejecución del sistema

### Interfaz gráfica

Para iniciar la aplicación interactiva:

```cmd
.venv\Scripts\python.exe -m streamlit run app.py
```

La aplicación permite:

- Visualizar los escenarios logísticos.
- Seleccionar algoritmos de búsqueda.
- Comparar Greedy y A*.
- Ejecutar métodos de optimización.
- Consultar análisis de teoría de juegos.
- Ejecutar Minimax y poda alfa-beta.
- Consultar y descargar resultados experimentales.

### Ejecución desde consola

También es posible ejecutar el flujo principal:

```cmd
.venv\Scripts\python.exe main.py
```

Este proceso ejecuta los módulos algorítmicos y genera los resultados experimentales correspondientes.

## 8. Pruebas del sistema

Para ejecutar las pruebas automatizadas:

```cmd
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas contemplan:

- Validación de dimensiones del escenario.
- Búsqueda de rutas mediante A* y Greedy.
- Evaluación de múltiples escenarios.
- Validación de algoritmos incorrectos.
- Detección de escenarios sin solución.
- Ejecuciones de Hill Climbing.
- Comprobación de equilibrios de Nash.
- Comparación entre Minimax y poda alfa-beta.

## 9. Experimentos y resultados

Los experimentos se almacenan en la carpeta `experiments/`.

| Archivo | Contenido |
|---|---|
| resultados.csv | Registros de ejecuciones experimentales |
| resumen.csv | Estadísticas comparativas |
| comparacion_evaluaciones.png | Visualización de métricas |

Las métricas utilizadas incluyen:

- Costo de solución.
- Tiempo de ejecución.
- Nodos expandidos.
- Número de evaluaciones.
- Mejor resultado.
- Promedio.
- Desviación estándar.

Los resultados deben analizarse considerando los parámetros y las semillas aleatorias utilizados.

## 10. Modelo logístico y supuestos

El entorno utiliza una cuadrícula de 12 × 12 con movimientos ortogonales.

Se consideran los siguientes elementos:

- Almacén como punto de inicio.
- Tres puntos de entrega.
- Destino final.
- Obstáculos no transitables.
- Terrenos con costos de desplazamiento variables.
- Recursos limitados.
- Modelos estratégicos de competencia.

La heurística Manhattan se utiliza para estimar distancias y es admisible para A* bajo los costos mínimos y movimientos definidos.

Greedy prioriza la heurística, mientras que A* considera el costo acumulado y la estimación restante.

Los algoritmos de optimización trabajan sobre el orden de visita de las entregas, utilizando el costo de los recorridos entre paradas.

## 11. Limitaciones

- Los escenarios representan un entorno logístico sintético.
- Los resultados dependen de los parámetros y semillas configurados.
- Los pagos de teoría de juegos son supuestos definidos para el modelo.
- Minimax representa un subproblema simplificado de asignación de recursos.
- Las decisiones estratégicas se analizan junto con la planificación, pero sus resultados todavía no modifican automáticamente el mapa ni el costo de la ruta final.

## 12. Integración y trabajo futuro

El sistema comparte una representación común del escenario entre sus módulos algorítmicos.

Como mejoras futuras se contempla:

- Integrar dinámicamente las decisiones del competidor en los costos de desplazamiento.
- Incorporar restricciones de recursos directamente en la planificación.
- Ampliar la cantidad y complejidad de los escenarios.
- Mejorar la visualización de las comparaciones experimentales.
- Incorporar nuevos criterios de optimización.

## 13. Autor

**Desarrollado por:** Luis Javier Terrones Muñoz.

Proyecto académico desarrollado en Python como sistema inteligente de planificación, optimización y toma de decisiones adversarias.