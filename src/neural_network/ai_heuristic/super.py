import os

# Plot the line for each cube
import matplotlib.pyplot as plt

import random

import numpy as np
from tensorflow import keras

from src.modelisation.modelisation import Cube
from src.search.models.game_state import GameState

NUMBER_OF_INPUTS = 6 * 9 * 6

TESTING_SET_SIZE = 10000
TEST_RATIO = 0.8


def create_model() -> keras.Model:
    inputs = keras.Input(shape=(NUMBER_OF_INPUTS,))
    x = keras.layers.Dense(6, activation="sigmoid")(inputs)
    outputs = keras.layers.Dense(1, activation="linear")(x)
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss=keras.losses.MeanSquaredError(),
        metrics=["mse"],
    )

    return model


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
    model = create_model()
    model.summary()
    for i in range(TESTING_SET_SIZE):
        cube = Cube(3)
        scramble_level = random.randint(0, 20)
        cube.scramble(scramble_level)
        cube_data = get_cube_data_input(cube)
        trainings_inputs.append(cube_data)
        trainings_outputs.append(scramble_level)
    print("Finished creating training data")
    print("Training...")
    model.fit(
        trainings_inputs[:number_of_trainings],
        trainings_outputs[:number_of_trainings],
        epochs=1000,
        workers=16,
    )
    print("Testing...")
    test_loss, test_acc = model.evaluate(
        trainings_inputs[number_of_trainings:],
        trainings_outputs[number_of_trainings:],
        verbose=2,
    )
    print("Test accuracy:", test_acc)
    print("Test loss:", test_loss)

    # save model
    model.save(path)
    return model


def evaluate_cube(cube: Cube):
    model_path = r"C:\Users\gaspa\Documents\Dev\ULB\pyrubik\src\neural_network\ai_heuristic\model.h5"

    if not os.path.isfile(model_path):
        model = get_trained_model(model_path)
    else:
        model = keras.models.load_model(model_path)

    cube_data = get_cube_data_input(cube)

    return model.predict(np.array([cube_data]))[0][0]


def deep_learning_evaluate_function(state: GameState) -> float:
    """
    Evaluation function based on a deep learning model.
    """
    return evaluate_cube(state.cube)


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