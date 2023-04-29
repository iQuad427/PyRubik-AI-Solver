import json
import os

from sklearn.tree import DecisionTreeRegressor

from src.evaluation.ml.generic import evaluate_model_for_cube
from src.modelisation.modelisation import Cube
from src.search.models.game_state import GameState

DTR_REGRESSOR_PARAMS = json.dumps(dict(max_depth=10))

PATH = os.path.join(os.path.dirname(__file__), "models", "dtr_regressor.json")


def dtr_regressor_evaluation_function(game_state: GameState) -> float:
    """
    Evaluate the game state using the DTR model.

    :param game_state: the game state to evaluate
    :return: the evaluation
    """

    return evaluate_model_for_cube(
        game_state.cube, DecisionTreeRegressor, DTR_REGRESSOR_PARAMS, PATH
    )


if __name__ == "__main__":
    score = []
    for i in range(50):
        cube = Cube(3)
        cube.scramble(i)
        score.append(dtr_regressor_evaluation_function(GameState(cube)))

    # Plot score evolution
    import matplotlib.pyplot as plt

    plt.plot(score)
    plt.show()
