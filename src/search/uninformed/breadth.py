import math
from typing import Callable

from src.search.generic.container_based import ContainerBasedGameEngine
from src.search.models.game_state import GameState


class BreadthFirstSearchEngine(ContainerBasedGameEngine):
    """
    Breadth First Search Engine

    This engine will search for a solution by exploring the shallowest nodes in the search tree first.
    """

    def __init__(
        self,
        starting_state: GameState,
        evaluation_function: Callable[[GameState], int],
        max_depth=math.inf,
    ):
        super().__init__(
            lambda state, container, _: container.append(state),
            starting_state,
            evaluation_function,
            max_depth,
        )
