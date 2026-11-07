"""Carga y validacion del escenario logistico compartido."""
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class Scenario:
    name: str
    size: int
    start: tuple
    final_destination: tuple
    deliveries: list
    obstacles: set
    rough_cells: set
    rough_cost: int
    default_cost: int
    initial_budget: int
    resource_capacity: int
    directions: tuple

    @classmethod
    def from_json(cls, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        size = int(data["size"])
        start = tuple(data["start"])
        goal = tuple(data["final_destination"])
        deliveries = [tuple(p) for p in data["deliveries"]]
        obstacles = {tuple(p) for p in data["obstacles"]}
        terrain = data["terrain_costs"]
        rough = {tuple(p) for p in terrain["rough_cells"]}
        obj = cls(
            data["name"], size, start, goal, deliveries, obstacles, rough,
            int(terrain["rough_cost"]), int(terrain["default"]),
            int(data["resources"]["initial_budget"]),
            int(data["resources"]["resource_capacity"]),
            tuple(tuple(d) for d in data["movement"]["directions"])
        )
        obj.validate()
        return obj

    def validate(self):
        def inside(p):
            return len(p) == 2 and all(isinstance(v, int) for v in p) and 0 <= p[0] < self.size and 0 <= p[1] < self.size
        points = [self.start, self.final_destination, *self.deliveries, *self.obstacles, *self.rough_cells]
        if self.size < 2 or not all(inside(p) for p in points):
            raise ValueError("Hay coordenadas fuera de la cuadrícula o dimensiones invalidas.")
        if self.start in self.obstacles or self.final_destination in self.obstacles:
            raise ValueError("El inicio y el destino final no pueden ser obstaculos.")
        if self.start == self.final_destination:
            raise ValueError("El inicio y el destino final deben ser distintos.")
        if self.start in self.deliveries or self.final_destination in self.deliveries:
            raise ValueError("Las entregas deben ser distintas del inicio y del destino final.")
        if any(p in self.obstacles for p in self.deliveries):
            raise ValueError("Un punto de entrega no puede ser un obstaculo.")
        if len(set(self.deliveries)) != len(self.deliveries):
            raise ValueError("Hay puntos de entrega duplicados.")
        if self.default_cost <= 0 or self.rough_cost < self.default_cost:
            raise ValueError("Los costos deben ser positivos y el terreno dificil no puede ser mas barato.")
        if any(p in self.obstacles for p in self.rough_cells):
            raise ValueError("Una celda de terreno dificil no puede ser tambien un obstaculo.")
        if not self.directions:
            raise ValueError("Debe existir al menos un movimiento permitido.")
        if any(len(d) != 2 or d == (0, 0) for d in self.directions):
            raise ValueError("Cada movimiento debe ser un desplazamiento valido de dos coordenadas.")
        if self.initial_budget < 0 or self.resource_capacity < 0:
            raise ValueError("Los recursos no pueden tener valores negativos.")

    def cost(self, cell):
        return self.rough_cost if cell in self.rough_cells else self.default_cost

    def neighbors(self, cell):
        r, c = cell
        for dr, dc in self.directions:
            nxt = (r + dr, c + dc)
            if 0 <= nxt[0] < self.size and 0 <= nxt[1] < self.size and nxt not in self.obstacles:
                yield nxt
