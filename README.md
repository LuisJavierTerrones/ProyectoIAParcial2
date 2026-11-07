# LogiSmart AI
Sistema inteligente de planificacion, optimizacion y toma de decisiones adversarias.

## Requisitos
- Python 3.10 o superior (recomendado 3.11/3.12).
- Bibliotecas: numpy, pandas, matplotlib, networkx.

## Instalacion en Windows
Abre PowerShell o la terminal de VS Code en la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si PowerShell bloquea `Activate.ps1`, no es necesario activar el entorno. Ejecuta directamente:
```powershell
.\.venv\Scripts\python.exe main.py
```

Alternativa CMD:
```cmd
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python main.py
```

## Ejecucion
```bash
python main.py
```
El programa imprime resultados de los cinco modulos, muestra una visualizacion del mapa y guarda `experiments/resultados.csv` y `experiments/resumen.csv`.

## Pruebas
```bash
python -m unittest discover -s tests -v
```

## Uso en Google Colab
1. Sube el ZIP del proyecto a Colab y descomprimelo.
2. En una celda, cambia al directorio extraido.
3. Ejecuta:
```python
%pip install -r requirements.txt
!python main.py
```
Tambien se incluye `LogiSmart_AI_Colab.ipynb`.

## Estructura
- `config/`: escenario y parametros externos en JSON.
- `logismart/scenario.py`: representacion y validacion compartida.
- `logismart/algorithms/`: implementaciones de busqueda, optimizacion y juegos.
- `logismart/experiments.py`: ejecuciones repetidas y CSV.
- `tests/`: pruebas automatizadas.
- `main.py`: flujo de ejecucion integrado.

## Modelo y supuestos
- Cuadricula de 12x12, movimientos ortogonales, sin diagonales.
- Entrar a una celda cuesta 1; el terreno dificil cuesta 3.
- Obstaculos no transitables.
- El costo del recorrido de entregas se calcula concatenando caminos optimos A* entre paradas consecutivas.
- Hill Climbing, recocido simulado y algoritmo genetico optimizan el orden de visita, no el movimiento dentro de cada tramo.
- La heuristica Manhattan es admisible para A* porque el costo minimo por movimiento es 1 y no se permiten diagonales.
- Greedy prioriza h(n), por lo que no garantiza costo optimo.
- El juego estatico y el subproblema minimax son modelos didacticos de decisiones estrategicas; sus pagos/utilidades son supuestos parametrizados para este escenario, no datos empiricos de una empresa real.

## Limitaciones que deben explicarse
- El escenario es sintetico y pequeno.
- El modelo de recursos y competencia es una abstraccion.
- Los resultados dependen de la semilla y parametros.
- El modulo de teoria de juegos usa pagos definidos en el codigo.
- Minimax modela una secuencia simplificada de asignacion/disputa de recursos.

## Trazabilidad
Los resultados experimentales se generan al ejecutar el programa. No se incluyen resultados simulados como si fueran mediciones reales. Registra version de Python, fecha, parametros y semilla al realizar la ejecucion final.


## Resultados verificados de la revisión
- Se ejecutaron 9 pruebas automatizadas; todas aprobaron.
- Los tres escenarios de 12x12 encontraron ruta con Greedy y A*.
- En la instancia base, ambos encontraron costo 22 para el trayecto directo inicio-destino.
- El recorrido que visita las tres entregas en el orden configurado tuvo costo 36.
- En las ejecuciones de optimización, los tres métodos obtuvieron costo 34.
- Los CSV se regeneran al ejecutar `python main.py`; los tiempos dependen del equipo y no deben compararse como constantes universales.

## Alcance de la integración y limitaciones
Los cinco módulos comparten el objeto `Scenario` y la configuración externa. El planificador de rutas y los optimizadores calculan el costo del orden de entregas; teoría de juegos y minimax analizan decisiones estratégicas con modelos didácticos. En esta versión, las salidas estratégicas se reportan junto con el plan, pero todavía no modifican automáticamente el mapa ni el costo de la ruta. Por tanto, no se debe afirmar que el competidor ya altera dinámicamente la ruta final. Esta es una mejora futura recomendada para satisfacer de forma más estricta la integración adversaria solicitada.

La búsqueda multi-parada suma rutas A* entre paradas consecutivas. La optimalidad de cada tramo no garantiza por sí sola que el orden global de entregas sea óptimo; ese orden es lo que intentan mejorar Hill Climbing y las metaheurísticas.


## Interfaz gráfica (recomendada para la demostración)

El proyecto incluye `app.py`, una interfaz web local desarrollada con Streamlit que llama a los módulos reales de `logismart/`. Permite visualizar el mapa, cambiar entre escenarios, ejecutar Greedy/A*, comparar algoritmos, ejecutar optimizadores, consultar teoría de juegos y Minimax, y descargar los CSV experimentales.

### Ejecutar la interfaz

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Se abrirá una pestaña del navegador en una dirección local (normalmente `http://localhost:8501`). La interfaz no sustituye `main.py`: ambos puntos de entrada usan las mismas implementaciones algorítmicas.
