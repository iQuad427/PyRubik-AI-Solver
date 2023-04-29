import json
import os

from sklearn.ensemble import RandomForestRegressor

from src.evaluation.ml.generic import evaluate_model_for_cube
from src.search.models.game_state import GameState

RANDOM_FOREST_REGRESSOR_PARAMS = json.dumps(
    dict(n_estimators=50, max_depth=10, random_state=0, n_jobs=-1)
)

PATH = os.path.join(os.path.dirname(__file__), "models", "rf_regressor.json")


def random_forest_regressor_evaluation_function(game_state: GameState) -> float:
    """
    Evaluate the game state using the RandomForestRegressor model.

    :param game_state: the game state to evaluate
    :return: the evaluation
    """

    return evaluate_model_for_cube(
        game_state.cube, RandomForestRegressor, RANDOM_FOREST_REGRESSOR_PARAMS, PATH
    )
