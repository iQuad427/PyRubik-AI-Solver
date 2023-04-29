from src.evaluation.ml.decision_tree_regressor import dtr_regressor_evaluation_function
from src.evaluation.ml.gradient_booster_regressor import (
    gbr_regressor_evaluation_function,
)
from src.evaluation.ml.neural_network_regressor import nnr_regressor_evaluation_function
from src.evaluation.ml.random_forest import random_forest_regressor_evaluation_function
from src.evaluation.ml.support_vector_regression import (
    svr_regressor_evaluation_function,
)
from src.evaluation.ml.xgb_regressor import xgb_regressor_evaluation_function

ML_EVALUATION_FUNCTIONS = {
    "Gradient Booster Regressor": gbr_regressor_evaluation_function,
    "Support Vector Regression": svr_regressor_evaluation_function,
    "XGB Regressor": xgb_regressor_evaluation_function,
    # "Random Forest Regressor": random_forest_regressor_evaluation_function,
    "Decision Tree Regressor": dtr_regressor_evaluation_function,
    "Neural Network Regressor": nnr_regressor_evaluation_function,
}
