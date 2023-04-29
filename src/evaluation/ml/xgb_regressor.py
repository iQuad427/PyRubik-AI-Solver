import json
import os

from xgboost import XGBRegressor

from src.evaluation.ml.generic import evaluate_model_for_cube
from src.search.models.game_state import GameState

XGB_REGRESSOR_PARAMS = json.dumps(
    dict(
        booster="gbtree",
        colsample_bytree=0.8,
        eta=0.3,
        gamma=0,
        max_depth=10,
        max_leaves=511,
        n_estimators=50,
        objective="reg:logistic",
        reg_alpha=0.8333333333333334,
        reg_lambda=1.9791666666666667,
        subsample=1,
        tree_method="auto",
        n_jobs=-1,
    )
)

PATH = os.path.join(os.path.dirname(__file__), "models", "xgb_regressor.json")


def xgb_regressor_evaluation_function(game_state: GameState) -> float:
    """
    Evaluate the game state using the XGBRegressor model.

    :param game_state: the game state to evaluate
    :return: the evaluation
    """

    return evaluate_model_for_cube(
        game_state.cube, XGBRegressor, XGB_REGRESSOR_PARAMS, PATH
    )
