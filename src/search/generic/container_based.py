import math
from typing import Callable, List

from src.search.generic.generic import GenericGameEngine
from src.search.models.game_state import GameState


class ContainerBasedGameEngine(GenericGameEngine):
    """
    Container Based Game Engine

    This engine will search for a solution by exploring the nodes in the search tree using a container.
    It is quite generic, and can be used to implement any search algorithm that uses a container (list, queue, stack, etc)
    """

    def __init__(
        self,
        insert_to_container: Callable[[GameState, List, int], None],
        starting_state: GameState,
        evaluation_function: Callable[[GameState], int],
        max_depth=math.inf,
        container_generator: Callable = list,
        get_next_state: Callable[[List], GameState] = lambda x: x.pop(0),
    ):
        super().__init__(starting_state, evaluation_function, max_depth)
        self.insert_to_container = insert_to_container
        self.container_generator = container_generator
        self.get_next_state = get_next_state
        self.best_founds = []
        self.best_scores = []

    def run(self):
        container = self.container_generator()
        self.insert_to_container(self.state, container, 0)

        while container:
            # Remove previous print
            state = self.get_next_state(container)
            score = self.evaluation_function(state)

            print(self.best_scores)

            if score == 0:
                print(score)
                print(state.cube)
                return state

            if len(self.best_scores) < 8:
                self.best_founds.append(state)
                self.best_scores.append(score)
            elif score < max(self.best_scores):
                index_to_remove = self.best_scores.index(max(self.best_scores))
                self.best_founds[index_to_remove] = state
                self.best_scores[index_to_remove] = score

            if state.depth < self.max_depth:
                for action in state.get_legal_actions():
                    self.insert_to_container(
                        state.generate_successor([action]),
                        container,
                        score,
                    )

        return None
