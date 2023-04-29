import json
import os

from sklearn.svm import SVR

from src.evaluation.ml.generic import evaluate_model_for_cube
from src.search.models.game_state import GameState

SVR_REGRESSOR_PARAMS = json.dumps(dict(kernel="linear"))

PATH = os.path.join(os.path.dirname(__file__), "models", "svr_regressor.json")


def svr_regressor_evaluation_function(game_state: GameState) -> float:
    """
    Evaluate the game state using the SVR model.

    :param game_state: the game state to evaluate
    :return: the evaluation
    """

    return evaluate_model_for_cube(game_state.cube, SVR, SVR_REGRESSOR_PARAMS, PATH)
