# Informe tecnico - LogiSmart AI

> Completa los campos entre corchetes y pega resultados reales generados por el programa. No inventes mediciones.

## 1. Portada y resumen ejecutivo
**Institucion:** [Nombre]  
**Asignatura:** [Asignatura]  
**Estudiante:** [Nombre]  
**Docente:** [Nombre]  
**Fecha:** [Fecha]

**Resumen:** LogiSmart AI integra cinco enfoques de IA para planificar rutas, ordenar entregas y analizar decisiones estrategicas en un escenario logistico sintetico de 12x12.

## 2. Planteamiento del problema y supuestos
Se modela una red logistica en una cuadricula de 12x12 con almacen, tres entregas, destino final, obstaculos y costos de terreno variables. El objetivo es encontrar rutas de bajo costo y analizar la asignacion de recursos ante un competidor.

Supuestos: movimientos ortogonales; costos positivos; obstaculos bloquean el paso; el terreno dificil cuesta mas; las entregas deben visitarse una vez antes del destino final.

## 3. Arquitectura e integracion
Describe `Scenario`, archivos JSON, modulos y flujo desde `main.py`. Explica entradas/salidas de cada modulo.

## 4. Fundamento y diseno de algoritmos
### 4.1 Greedy Best-First Search
Prioriza h(n), con h Manhattan. No garantiza optimalidad.

### 4.2 A*
Prioriza f(n)=g(n)+h(n). Manhattan es admisible bajo movimientos ortogonales y costo minimo unitario.

### 4.3 Hill Climbing
Solucion: permutacion de entregas. Vecindad: intercambio de dos posiciones. Se ejecutan diez inicios.

### 4.4 Recocido simulado
Acepta mejoras y, con probabilidad exp(-delta/T), algunos empeoramientos. La temperatura disminuye multiplicandose por una tasa de enfriamiento.

### 4.5 Algoritmo genetico
Individuos son permutaciones. Usa torneo, cruce por orden, mutacion por intercambio y elitismo.

### 4.6 Teoria de juegos
Juego estatico 3x3. Las matrices de pagos son supuestos ilustrativos. Reporta mejores respuestas y equilibrios puros calculados.

### 4.7 Minimax y alfa-beta
Juego por turnos de asignacion/disputa de unidades. MAX y MIN alternan. Compara el valor y nodos explorados.

## 5. Diseno experimental y parametros
Incluye version de Python, sistema, semilla, parametros JSON y fecha de ejecucion. Justifica los presupuestos de ejecucion.

## 6. Resultados cuantitativos y visualizaciones
Inserta tablas de `experiments/resultados.csv`, `experiments/resumen.csv` y graficas producidas por ejecuciones reales.

## 7. Analisis comparativo y discusion
Compara calidad de solucion, variabilidad, evaluaciones y tiempo. Distingue costo de ruta, nodos expandidos y tiempo.

## 8. Pruebas, limitaciones y amenazas a la validez
Incluye salida de pruebas unitarias. Discute escenario sintetico, parametros, modelo de pagos y simplificaciones.

## 9. Conclusiones y trabajo futuro
Redacta conclusiones basadas en resultados observados, no en expectativas.

## 10. Referencias y anexos tecnicos
Documenta fuentes consultadas y adjunta configuraciones, CSV, capturas y comandos reproducibles.
