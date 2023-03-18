import math
from typing import Callable

from src.search.generic.container_based import ContainerBasedGameEngine
from src.search.models.game_state import GameState


class PriorityQueue:
    """
    Priority Queue

    This is a simple implementation of a priority queue. Not the most efficient one, but it works.
    """

    def __init__(self):
        self._queue = []

    def __bool__(self):
        return bool(self._queue)

    def put(self, priority, item):
        self._queue.append((priority, item))
        self._queue.sort(key=lambda x: x[0])

    def get(self):
        return self._queue.pop(0)[1]


class AStarSearchEngine(ContainerBasedGameEngine):
    """
    A* Search Engine

    This engine will search for a solution by exploring the nodes with the lowest evaluation function.
    """

    def __init__(
        self,
        starting_state: GameState,
        evaluation_function: Callable[[GameState], int],
        max_depth=math.inf,
    ):
        super().__init__(
            lambda state, container, score: container.put(score, state),
            starting_state,
            evaluation_function,
            max_depth,
            container_generator=PriorityQueue,
            get_next_state=lambda x: x.get(),
        )
