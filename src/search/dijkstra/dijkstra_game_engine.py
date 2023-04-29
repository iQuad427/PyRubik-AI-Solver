import heapq
import math
from typing import Callable

from src.modelisation.modelisation import Cube, final_position
from src.search.models.game_state import GameState


class DijkstraGameEngine:
    """
    Dijkstra Game Engine

    A game engine that uses Dijkstra's algorithm to find the solution to a game.
    """

    def __init__(
        self,
        starting_state,
        evaluation_function: Callable[[GameState], int],
    ):
        self.starting_state = starting_state
        self.evaluation_function = evaluation_function

    def run(self):
        model = self.starting_state.cube

        best_score = math.inf
        distances = {str(model.cube): 0}

        heap = [(best_score, model.cube, [])]
        heapq.heapify(heap)

        while len(heap) != 0:
            current = heapq.heappop(heap)
            # print(current)

            if current[0] < best_score:
                best_score = current[0]

            if final_position(current[1]):
                return current[2]

            for move in model.perms:
                distance = distances[str(current[1])] + 1
                next_state = Cube(model.n, inner=current[1]).permute([move])

                hashable = str(next_state.cube)

                if hashable not in distances or distances[hashable] > distance:
                    heapq.heappush(
                        heap,
                        (
                            (distance + 1) ** 2
                            * self.evaluation_function(GameState(next_state)),
                            next_state.cube,
                            current[2] + [move],
                        ),
                    )
                    distances[hashable] = distance

    def __str__(self):
        return self.__class__.__name__
