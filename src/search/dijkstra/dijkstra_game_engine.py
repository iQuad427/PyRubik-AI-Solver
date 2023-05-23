import heapq
import math
from typing import Callable

from src.modelisation.modelisation import Cube, final_position
from src.search.models.game_state import GameState
from src.modelisation.data import scrambled_3, stagnate_3


class DijkstraGameEngine:
    """
    Dijkstra Game Engine

    A game engine that uses Dijkstra's algorithm to find the solution to a game.
    """

    def __init__(
            self,
            starting_state,
            evaluation_function: Callable[[GameState], int]
    ):
        self.starting_state = starting_state
        self.evaluation_function = evaluation_function

        weight = evaluation_function(GameState(Cube(3, inner=scrambled_3)))

        # size = self.starting_state.cube.n
        # stagnation_points = evaluation_function(GameState(Cube(size, inner=eval(f"stagnate_{size}"))))
        # weight = stagnation_points / 20
        #
        # self.distance_weighting = lambda x: x * weight
        # self.distance_heuristic_link = lambda x, y: x + y

        if weight < 1:
            self.distance_weighting = lambda x: 0
            self.distance_heuristic_link = lambda x, y: x + y
        elif weight < 1_000:
            self.distance_weighting = lambda x: 2 * x
            self.distance_heuristic_link = lambda x, y: x + y
        elif weight < 100_000:
            self.distance_weighting = lambda x: x ** 2
            self.distance_heuristic_link = lambda x, y: x + y
        elif weight < 1_000_000:
            self.distance_weighting = lambda x: x + 1
            self.distance_heuristic_link = lambda x, y: x * y
        else:
            self.distance_weighting = lambda x: (1 + x) ** 2
            self.distance_heuristic_link = lambda x, y: x * y

    def run(self):
        model = self.starting_state.cube

        best_score = math.inf
        distances = {str(model.cube): 0}

        heap = [(best_score, model.cube, [])]
        heapq.heapify(heap)

        while len(heap) != 0:
            current = heapq.heappop(heap)

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
                            self.distance_heuristic_link(
                                self.distance_weighting(distance),
                                self.evaluation_function(GameState(next_state))
                            ),
                            next_state.cube,
                            current[2] + [move],
                        ),
                    )
                    distances[hashable] = distance

    def __str__(self):
        return self.__class__.__name__
