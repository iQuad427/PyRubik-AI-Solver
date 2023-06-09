import math
from typing import Callable

from src.search.generic.generic import GenericGameEngine
from src.search.models.game_state import GameState
from src.search.uninformed.depth import DepthFirstSearchEngine


class IterativeDeepeningSearchEngine(GenericGameEngine):
    """
    Iterative Deepening Search Engine

    This engine will search for a solution by exploring the deepest nodes in the search tree first.
    But it will do it iteratively, increasing the depth of the search tree at each iteration.
    """

    def __init__(
        self,
        starting_state: GameState,
        evaluation_function: Callable[[GameState], int],
        max_depth=math.inf,
    ):
        super().__init__(starting_state, evaluation_function, max_depth)

        self.best_found = None
        self.best_score = math.inf

    def run(self):

        for depth in range(self.max_depth):
            engine = DepthFirstSearchEngine(self.state, self.evaluation_function, depth)
            solution = engine.run()

            if min(engine.best_scores) < self.best_score:
                self.best_found = engine.best_founds[
                    engine.best_scores.index(min(engine.best_scores))
                ]
                self.best_score = min(engine.best_scores)

            if solution is not None:
                return solution

        return None
