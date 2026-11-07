# Informe técnico — LogiSmart AI
## Sistema inteligente de planificación, optimización y toma de decisiones adversarias

**Institución:** [Completar]  
**Asignatura:** [Completar]  
**Estudiante:** [Completar]  
**Docente:** [Completar]  
**Fecha de ejecución revisada:** 6 de noviembre de 2026

## 1. Resumen ejecutivo
LogiSmart AI es un prototipo en Python que representa una red logística mediante una cuadrícula de 12 × 12. Integra búsqueda heurística (Greedy y A*), búsqueda local (Hill Climbing), metaheurísticas (recocido simulado y algoritmo genético), teoría de juegos y búsqueda adversaria (Minimax y poda alfa-beta). La configuración se almacena en archivos JSON y las ejecuciones experimentales se exportan a CSV.

En la revisión se ejecutaron nueve pruebas automatizadas, todas aprobadas. En el escenario base, Greedy y A* encontraron una ruta directa de costo 22. La ruta que visita las tres entregas en el orden configurado tuvo costo 36. Los tres métodos de optimización del orden de entregas alcanzaron costo 34 en las ejecuciones registradas. Estos resultados corresponden a los escenarios y parámetros incluidos; no representan una garantía general de superioridad.

## 2. Planteamiento del problema y supuestos
Se modela una cuadrícula de 12 × 12 con almacén en (0,0), destino final en (11,11), tres entregas, obstáculos y celdas de terreno difícil. Los movimientos permitidos son ortogonales: arriba, abajo, izquierda y derecha. Entrar a una celda normal cuesta 1 y entrar a terreno difícil cuesta 3. Los obstáculos no son transitables.

El escenario incluye presupuesto inicial de 100 unidades y capacidad de recursos de 12 unidades. El costo de ruta se calcula sumando el costo de entrada a las celdas recorridas. Los archivos `config/escenario.json`, `escenario_2.json` y `escenario_3.json` describen tres configuraciones.

## 3. Arquitectura e integración
`Scenario` carga y valida el mapa compartido desde JSON. `pathfinding.py` implementa Greedy y A*. `local_search.py` optimiza el orden de las entregas con Hill Climbing. `metaheuristics.py` contiene recocido simulado y algoritmo genético. `game_theory.py` analiza un juego estático 3 × 3. `minimax.py` resuelve un subproblema adversario por turnos. `experiments.py` ejecuta pruebas repetidas y genera CSV. `main.py` coordina la ejecución.

Los módulos comparten la representación de escenario y sus resultados se muestran en una misma ejecución. **Límite de integración:** las decisiones de teoría de juegos y minimax se calculan y reportan, pero en esta versión no alteran automáticamente los costos del mapa, la disponibilidad de recursos del escenario ni la ruta final. Esta conexión dinámica queda como trabajo pendiente y debe reconocerse durante la defensa.

## 4. Fundamento y diseño de algoritmos
### 4.1 Greedy Best-First Search
Prioriza `h(n)`, aquí la distancia Manhattan al objetivo. Puede encontrar una ruta rápidamente, pero no garantiza el menor costo porque no considera el costo acumulado `g(n)` al ordenar la frontera.

### 4.2 A*
Prioriza `f(n)=g(n)+h(n)`. La distancia Manhattan es admisible para movimientos ortogonales cuando cada movimiento cuesta al menos 1: nunca sobreestima el costo restante. Con costos positivos y esta heurística consistente, A* encuentra una ruta óptima para cada tramo.

### 4.3 Hill Climbing
Cada candidato es una permutación de las tres entregas. La vecindad se construye intercambiando dos posiciones. En cada iteración se evalúan vecinos y se avanza al mejor si mejora el costo. Puede detenerse en óptimos locales o mesetas.

### 4.4 Recocido simulado
Parte de un orden aleatorio. Acepta mejoras y acepta soluciones peores con probabilidad `exp(-Δ/T)`, donde `Δ` es el incremento de costo y `T` la temperatura. La temperatura se multiplica por la tasa de enfriamiento en cada paso.

### 4.5 Algoritmo genético
Cada individuo representa un orden de entregas. Se utiliza selección por torneo, cruce por orden, mutación por intercambio y elitismo. El costo de ruta es la función objetivo.

### 4.6 Teoría de juegos
Se define un juego de dos jugadores con tres estrategias cada uno. Jugador A: conservadora, equilibrada y agresiva. Jugador B: no competir, promoción y bloquear recurso. Las matrices de pago son supuestos didácticos codificados en `game_theory.py`, no datos reales de una empresa. El análisis reportó un equilibrio de Nash puro: A agresiva y B promoción, con pagos (4,5). No se encontró estrategia dominante para ninguno de los jugadores.

### 4.7 Minimax y poda alfa-beta
El estado se representa mediante turnos restantes, unidades disponibles y puntuación. MAX y MIN alternan acciones legales; la utilidad evalúa la puntuación y los recursos remanentes. Alfa-beta evita explorar ramas que no pueden mejorar la decisión. En la configuración revisada ambos algoritmos devolvieron el mismo valor minimax.

## 5. Diseño experimental y parámetros
La semilla general es 42. Hill Climbing utiliza 10 soluciones iniciales y un máximo de 500 iteraciones. Recocido simulado realiza 20 ejecuciones, con temperatura inicial 100, enfriamiento 0.995 y temperatura mínima 0.01. El algoritmo genético realiza 20 ejecuciones con población 40, 150 generaciones, cruce 0.85, mutación 0.15 y torneo de tamaño 3. Minimax usa profundidad 6.

Los parámetros se encuentran en `config/parametros.json`. Los tiempos medidos dependen del hardware, carga del sistema y entorno de ejecución.

## 6. Resultados cuantitativos
### 6.1 Búsqueda heurística
| Escenario | Greedy costo | Greedy expandidos | A* costo | A* expandidos |
|---|---:|---:|---:|---:|
| Base | 22 | 22 | 22 | 75 |
| Variante 2 | 22 | 22 | 22 | 90 |
| Variante 3 | 22 | 22 | 22 | 123 |

En estas instancias ambos encontraron el mismo costo para la ruta directa. Greedy expandió menos nodos, pero esto no demuestra optimalidad general; A* utiliza el costo acumulado y la heurística admisible para garantizar optimalidad por tramo bajo los supuestos descritos.

### 6.2 Optimización del orden de entregas
| Método | Mejor costo | Promedio | Desviación estándar | Evaluaciones promedio | Tiempo promedio (s) |
|---|---:|---:|---:|---:|---:|
| Hill Climbing | 34 | 34 | 0 | 6.4 | 0.00115 |
| Recocido simulado | 34 | 34 | 0 | 1839 | 0.00324 |
| Algoritmo genético | 34 | 34 | 0 | 5890 | 0.03947 |

Los tres métodos alcanzaron costo 34 en las ejecuciones revisadas. La desviación estándar cero indica que no hubo variación en el costo final de esta muestra. No significa que los métodos sean equivalentes: utilizaron cantidades distintas de evaluaciones y tiempos. Para estudiar mejor su comportamiento se recomienda incorporar mapas más variados, más entregas y costos/obstáculos que generen diferencias entre permutaciones.

### 6.3 Teoría de juegos
El análisis encontró un equilibrio puro: estrategia agresiva para la empresa y promoción para el competidor. Los pagos correspondientes son 4 y 5. No hay estrategias dominantes en las matrices actuales.

### 6.4 Minimax y alfa-beta
| Métrica | Minimax | Alfa-beta |
|---|---:|---:|
| Valor calculado | 0 | 0 |
| Nodos visitados | 4984 | 3911 |
| Ramas podadas | — | 308 |

Ambos métodos calcularon el mismo valor. Alfa-beta visitó menos nodos, lo que evidencia el efecto de la poda en este árbol y orden de acciones.

## 7. Análisis comparativo y discusión
A* y Greedy encontraron rutas de costo 22 en los tres escenarios directos. Greedy expandió menos nodos en estas pruebas, pero no garantiza una solución de costo mínimo. A* realizó más expansiones y ofrece la garantía de optimalidad por tramo con la heurística definida.

En la optimización del orden de entregas, todos los métodos obtuvieron costo 34. Hill Climbing necesitó menos evaluaciones en este caso; recocido simulado y algoritmo genético realizaron más trabajo. El resultado sugiere que el problema de tres entregas es pequeño para distinguir la capacidad de exploración de los métodos. Conviene ampliar el número de entregas y diseñar escenarios con diferencias de costo más pronunciadas.

## 8. Pruebas, limitaciones y amenazas a la validez
La batería de pruebas revisada contiene nueve pruebas: dimensiones del mapa, ruta A*, rutas en tres escenarios, ruta Greedy, rechazo de algoritmo inválido, detección de escenario sin solución, métricas de Hill Climbing, reporte de Nash y equivalencia Minimax/alfa-beta. Resultado: **9 pruebas aprobadas**.

Limitaciones: escenarios sintéticos; matrices de pago asumidas; modelo simplificado de competencia; el resultado estratégico aún no modifica la ruta; pocos puntos de entrega; tiempos muy pequeños sensibles al entorno. La ruta multi-parada suma caminos óptimos entre paradas, mientras las metaheurísticas buscan mejorar el orden global.

## 9. Conclusiones y trabajo futuro
LogiSmart AI integra las cinco familias de técnicas solicitadas y permite ejecutar experimentos reproducibles con semilla y parámetros externos. En las pruebas realizadas, A* encontró rutas directas de costo 22; los optimizadores alcanzaron costo 34 para el orden de entregas; y alfa-beta obtuvo el mismo valor que Minimax visitando menos nodos.

El siguiente paso más importante es conectar la decisión del competidor con la disponibilidad o costo de recursos y recalcular la planificación final. También se recomienda ampliar escenarios, agregar más entregas, medir sistemáticamente la variabilidad y fortalecer pruebas de restricciones y casos límite.

## 10. Referencias y anexos técnicos
- Russell, S. y Norvig, P. *Artificial Intelligence: A Modern Approach*. Referencia general para búsqueda heurística y adversaria.
- Documentación oficial de Python: https://docs.python.org/3/
- Configuraciones JSON en `config/`.
- Resultados experimentales en `experiments/resultados.csv` y `experiments/resumen.csv`.
- Código fuente, pruebas y notebook incluidos en el repositorio comprimido.
