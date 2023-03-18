import math
from typing import Callable

from src.search.models.game_state import GameState


class GenericGameEngine:
    """
    Generic Game Engine

    The raw skeleton of a game engine. It will be used as a base class for all the other game engines.
    """

    def __init__(
        self,
        starting_state: GameState,
        evaluation_function: Callable[[GameState], int],
        max_depth=math.inf,
    ):
        self.state = starting_state
        self.evaluation_function = evaluation_function
        self.max_depth = max_depth

    def run(self):
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__
