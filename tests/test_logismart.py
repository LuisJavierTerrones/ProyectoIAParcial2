import unittest
from pathlib import Path
from logismart.scenario import Scenario
from logismart.algorithms.pathfinding import search
from logismart.algorithms.local_search import multiple_starts
from logismart.algorithms.game_theory import analyze_game
from logismart.algorithms.minimax import compare

ROOT = Path(__file__).resolve().parents[1]

class LogiSmartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenario = Scenario.from_json(ROOT / "config" / "escenario.json")

    def test_grid_dimensions(self):
        self.assertEqual(self.scenario.size, 12)

    def test_astar_finds_route(self):
        result = search(self.scenario, self.scenario.start,
                        self.scenario.final_destination, "astar")
        self.assertTrue(result["found"])
        self.assertGreater(result["cost"], 0)

    def test_three_scenarios_are_solvable(self):
        for filename in ("escenario.json", "escenario_2.json", "escenario_3.json"):
            scenario = Scenario.from_json(ROOT / "config" / filename)
            self.assertTrue(search(scenario, scenario.start,
                                   scenario.final_destination, "astar")["found"])

    def test_greedy_finds_route(self):
        self.assertTrue(search(self.scenario, self.scenario.start,
                               self.scenario.final_destination, "greedy")["found"])

    def test_invalid_algorithm_rejected(self):
        with self.assertRaises(ValueError):
            search(self.scenario, self.scenario.start,
                   self.scenario.final_destination, "bfs")

    def test_no_solution_reported(self):
        import copy
        isolated = copy.deepcopy(self.scenario)
        isolated.obstacles = {(r, 5) for r in range(12)}
        result = search(isolated, (0, 0), (0, 11), "astar")
        self.assertFalse(result["found"])

    def test_hill_climbing_multiple_starts_and_metrics(self):
        results = multiple_starts(self.scenario, count=10, seed=42)
        self.assertEqual(len(results), 10)
        for item in results:
            self.assertGreaterEqual(item["evaluations"], 1)
            self.assertGreaterEqual(item["time_seconds"], 0)

    def test_nash_is_reported(self):
        result = analyze_game()
        self.assertIsInstance(result["nash_pure"], list)
        self.assertEqual(len(result["nash_pure"]), 1)

    def test_minimax_alpha_beta_equal(self):
        result = compare(4)
        self.assertTrue(result["same_value"])
        self.assertLessEqual(result["alphabeta_nodes"], result["minimax_nodes"])

if __name__ == "__main__":
    unittest.main()
