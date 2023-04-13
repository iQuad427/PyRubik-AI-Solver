import unittest

from src.modelisation.modelisation import Cube
from src.search.evaluation.CFOP.cross import white_cross_evaluation
from src.search.models.game_state import GameState
from src.search.uninformed.iterative_depth import IterativeDeepeningSearchEngine


class TestCross(unittest.TestCase):

    def test_level_1(self):
        self.run_experiment_for_scramble(Cube(3).scramble(1))

    def test_level_2(self):
        self.run_experiment_for_scramble(Cube(3).scramble(2))

    def test_level_3(self):
        self.run_experiment_for_scramble(Cube(3).scramble(3))

    def test_level_4(self):
        self.run_experiment_for_scramble(Cube(3).scramble(4))

    def test_level_5(self):
        self.run_experiment_for_scramble(Cube(3).scramble(5))

    def test_level_6(self):
        self.run_experiment_for_scramble(Cube(3).scramble(6))

    def test_level_7(self):
        self.run_experiment_for_scramble(Cube(3).scramble(7))

    def test_level_8(self):
        self.run_experiment_for_scramble(Cube(3).scramble(8))

    def test_level_max(self):
        self.run_experiment_for_scramble(Cube(3).scramble(20))

    def run_experiment_for_scramble(self, scramble: list[str]):
        cube = Cube(3)
        cube = cube.permute(scramble)

        engine = IterativeDeepeningSearchEngine(
            starting_state=GameState(cube),
            evaluation_function=white_cross_evaluation,
            max_depth=16
        )

        solution = engine.run()

        self.assertEqual(white_cross_evaluation(solution), 0)


if __name__ == '__main__':
    unittest.main()
