import json
import os
import random
from functools import lru_cache
from typing import Type

import joblib
import numpy as np

from src.modelisation.modelisation import Cube

NUMBER_OF_INPUTS = 6 * 9 * 6
LEARNING_DATA_AMOUNT = 10000
TEST_RATIO = 0.8


def get_cube_data_input(cube: Cube) -> list:
    """
    Convert the cube to input data for the model.

    :param cube: the cube to convert
    :return: the input data
    """
    data = cube.int_list()
    input_data = []

    for element in data:
        a = list(np.zeros(6))
        a[element] = 1
        input_data.extend(a)

    return input_data


def get_trained_model(path: str, model_class: Type, model_params: dict):
    """
    Train the model and save it to disk.

    :param model_class:  the model class to use to train the model
    :param path: path to save the model to
    :return: the trained model
    """

    print("Launching model training for", model_class.__name__, "...")

    number_of_trainings = int(LEARNING_DATA_AMOUNT * TEST_RATIO)
    trainings_inputs = []
    trainings_outputs = []

    for _ in range(LEARNING_DATA_AMOUNT):
        cube = Cube(3)
        max_level = 20
        scramble_level = random.randint(0, max_level)
        cube.scramble(scramble_level)
        cube_data = get_cube_data_input(cube)
        trainings_inputs.append(cube_data)
        trainings_outputs.append(scramble_level / max_level)

    print("Finished creating training data")
    print("Training...")

    model = model_class(**model_params)

    model.fit(
        trainings_inputs[:number_of_trainings], trainings_outputs[:number_of_trainings]
    )

    # Evaluate model
    test_loss = model.score(
        trainings_inputs[number_of_trainings:], trainings_outputs[number_of_trainings:]
    )

    print("Test loss: ", test_loss)

    # save model
    try:
        model.save_model(path)
    except AttributeError:
        joblib.dump(model, path)

    return model


@lru_cache(maxsize=100)
def get_model(model_class: Type, model_params: str, path_to_model: str):
    """
    Get the trained model or train it if it doesn't exist.

    :param model_class: the model class to use to train the model
    :param model_params: the parameters to use to train the model
    :param path_to_model: path to save the model to
    """
    if not os.path.exists(path_to_model):
        return get_trained_model(path_to_model, model_class, json.loads(model_params))
    else:
        try:
            model = model_class()
            model.load_model(path_to_model)
        except AttributeError:
            model = joblib.load(path_to_model)
        return model


def evaluate_model_for_cube(
    cube: Cube, model_class: Type, model_params: str, path_to_model: str
):
    """
    Use the model to predict the scramble level of the cube.

    :param data: the cube data
    :param model_class: the model class to use to train the model
    :param model_params: the parameters to use to train the model
    :param path_to_model: path to save the model to
    :return: the scramble level
    """
    cube_data = np.array(get_cube_data_input(cube)).reshape(1, -1)
    return get_model(model_class, model_params, path_to_model).predict(cube_data)[0]
