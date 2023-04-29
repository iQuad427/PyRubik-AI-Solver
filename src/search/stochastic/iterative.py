from typing import Callable

from src.modelisation.modelisation import Cube
from src.search.generic.generic import GenericGameEngine
from src.search.models.game_state import GameState
from src.search.stochastic.best_improvement import BestImprovement


class IteratedLocalSearch(GenericGameEngine):
    def __init__(
        self, starting_state: GameState, evaluation_function: Callable[[GameState], int]
    ):
        super().__init__(starting_state, evaluation_function)

    def run(self):
        engine = BestImprovement(self.state, self.evaluation_function)
        current = engine.run()

        while not current:
            new = current.generate_successor(
                Cube(current.cube.n).scramble(3)
            )  # perturbation

            engine = BestImprovement(new, self.evaluation_function)
            new = engine.run()  # subsidiary local search

            if self.evaluation_function(new) < self.evaluation_function(current):
                current = new

        return current
