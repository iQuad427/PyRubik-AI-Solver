

from typing import Callable

from src.search.generic.generic import GenericGameEngine
from src.search.models.game_state import GameState


class BestImprovement(GenericGameEngine):
    def __init__(
            self,
            starting_state: GameState,
            evaluation_function: Callable[[GameState], int]):

        super().__init__(starting_state, evaluation_function)

    def run(self):
        current = self.state
        best = self.evaluation_function(current)
        improvement = True

        while improvement:
            improvement = False
            for move in self.state.cube.perms:
                if (score := self.evaluation_function(new := current.generate_successor([move]))) < best:
                    current = new
                    best = score
                    improvement = True

        return current
