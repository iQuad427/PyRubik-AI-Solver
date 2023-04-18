import os
import random
from functools import lru_cache
from typing import Tuple

from sklearn.pipeline import make_pipeline

# Plot the line for each cube
import matplotlib.pyplot as plt
import numpy as np
from xgboost import XGBRegressor

from src.modelisation.modelisation import Cube
from src.search.models.game_state import GameState

NUMBER_OF_INPUTS = 6 * 9 * 6

TESTING_SET_SIZE = 10000
TEST_RATIO = 0.8


def get_cube_data_input(cube: Cube):
    data = cube.int_list()
    input_data = []

    for element in data:
        a = list(np.zeros(6))
        a[element] = 1
        input_data.extend(a)

    return input_data


def get_trained_model(path: str):
    number_of_trainings = int(TESTING_SET_SIZE * TEST_RATIO)
    trainings_inputs = []
    trainings_outputs = []
    for i in range(TESTING_SET_SIZE):
        cube = Cube(3)
        max_level = 20
        scramble_level = random.randint(0, max_level)
        cube.scramble(scramble_level)
        cube_data = get_cube_data_input(cube)
        trainings_inputs.append(cube_data)
        trainings_outputs.append(scramble_level / max_level)
    print("Finished creating training data")
    print("Training...")

    # Create TruncatedSVD and XGBoostClassifier pipeline
    model = make_pipeline(
        XGBRegressor(
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

    model.fit(
        trainings_inputs[:number_of_trainings], trainings_outputs[:number_of_trainings]
    )

    print("Testing...")
    test_loss = model.score(
        trainings_inputs[number_of_trainings:], trainings_outputs[number_of_trainings:]
    )
    print("Test loss:", test_loss)

    # save model
    model.named_steps["xgbregressor"].save_model(path)
    return model.named_steps["xgbregressor"]


model_path = r"C:\Users\gaspa\Documents\Dev\ULB\pyrubik\src\neural_network\ai_heuristic\model.json"

if not os.path.isfile(model_path):
    model = get_trained_model(model_path)
else:
    model = XGBRegressor()
    model.load_model(model_path)


@lru_cache(maxsize=10000)
def inner_evaluate_cube(data: Tuple):
    cube_data = np.array(data).reshape(1, -1)
    # dimensionality reduction using TruncatedSVDWrapper
    return model.predict(cube_data)[0]


def evaluate_cube(cube: Cube):
    return inner_evaluate_cube(tuple(get_cube_data_input(cube)))


def deep_learning_evaluate_function(state: GameState) -> int:
    """
    Evaluation function based on a deep learning model.
    """
    return int(evaluate_cube(state.cube) * 100) ** 2


if __name__ == "__main__":

    results = []

    for i in range(50):
        cube = Cube(3)
        a = []
        for _ in range(30):
            cube.scramble(1)
            a.append(evaluate_cube(cube))

        results.append(a)

    # Plot median and mean lines
    plt.plot(np.mean(results, axis=0), label="Mean")
    plt.plot(np.median(results, axis=0), label="Median")
    # Plot confidence interval
    plt.fill_between(
        range(len(results[0])),
        np.quantile(results, 0.25, axis=0),
        np.quantile(results, 0.75, axis=0),
        alpha=0.5,
        label="Confidence interval",
    )

    plt.legend()
    plt.show()
