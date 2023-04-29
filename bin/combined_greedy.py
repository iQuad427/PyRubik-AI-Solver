from collections import defaultdict
from typing import Callable, List

from src.modelisation.modelisation import Cube
from src.search.dijkstra.dijkstra import dijkstra_search
from src.search.models.game_state import GameState

from src.evaluation.look_up import LOOK_UP_EVALUATION_FUNCTIONS
from src.evaluation.ml import ML_EVALUATION_FUNCTIONS
from src.evaluation.basic import BASIC_EVALUATION_FUNCTIONS


def normalize_evaluation_functions(evaluation_functions: List[Callable]):
    new_evaluation_functions = []

    for count, evaluation_function in enumerate(evaluation_functions):
        print("Preprocessing", evaluation_function.__name__, "...")
        scores = []

        for _ in range(10):
            for random_level in range(20):
                cube = Cube(3)
                cube.scramble(random_level)
                scores.append(evaluation_function(GameState(cube)))

        max_score = max(scores)

        new_evaluation_functions.append(
            lambda state, evaluation_function=evaluation_function, max_score=max_score: evaluation_function(
                state
            )
            / max_score
        )

    return new_evaluation_functions


def create_combined_evaluation_function(evaluation_functions: List[Callable]):
    normalized_evaluation_functions = normalize_evaluation_functions(
        evaluation_functions
    )

    def combined_evaluation_function(state: GameState):
        scores = []

        for evaluation_function in normalized_evaluation_functions:
            scores.append(evaluation_function(state))

        return sum(score**2 for score in scores)

    return combined_evaluation_function
