import math
from typing import Callable

from src.search.generic.generic import GenericGameEngine
from src.search.informed.a_star import AStarSearchEngine
from src.search.models.game_state import GameState


class IterativeDeepeningAStarSearchEngine(GenericGameEngine):
    """
    Iterative Deepening A* Search Engine

    This engine will search for a solution by exploring the nodes with the lowest evaluation function
    in the search tree first. But it will do it iteratively, increasing the depth of the search tree
    """

    def __init__(
        self,
        starting_state: GameState,
        evaluation_function: Callable[[GameState], int],
        max_depth=math.inf,
    ):
        super().__init__(starting_state, evaluation_function, max_depth)

    def run(self):
        for depth in range(self.max_depth):
            engine = AStarSearchEngine(self.state, self.evaluation_function, depth)
            solution = engine.run()

            if solution:
                return solution

        return None
