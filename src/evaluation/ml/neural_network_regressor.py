import json
import os

from sklearn.neural_network import MLPRegressor

from src.evaluation.ml.generic import evaluate_model_for_cube
from src.search.models.game_state import GameState

NNR_REGRESSOR_PARAMS = json.dumps(
    dict(hidden_layer_sizes=(100, 50), activation="relu", solver="adam", max_iter=1000)
)

PATH = os.path.join(os.path.dirname(__file__), "models", "nnr_regressor.json")


def nnr_regressor_evaluation_function(game_state: GameState) -> float:
    """
    Evaluate the game state using the NNR model.

    :param game_state: the game state to evaluate
    :return: the evaluation
    """

    return evaluate_model_for_cube(
        game_state.cube, MLPRegressor, NNR_REGRESSOR_PARAMS, PATH
    )
