import json
import os

from sklearn.ensemble import GradientBoostingRegressor

from src.evaluation.ml.generic import evaluate_model_for_cube
from src.search.models.game_state import GameState

GBR_REGRESSOR_PARAMS = json.dumps(
    dict(loss="huber", learning_rate=0.1, n_estimators=100, max_depth=3)
)

PATH = os.path.join(os.path.dirname(__file__), "models", "gbr_regressor.json")


def gbr_regressor_evaluation_function(game_state: GameState) -> float:
    """
    Evaluate the game state using the GBR model.

    :param game_state: the game state to evaluate
    :return: the evaluation
    """

    return evaluate_model_for_cube(
        game_state.cube, GradientBoostingRegressor, GBR_REGRESSOR_PARAMS, PATH
    )
