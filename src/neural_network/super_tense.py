import itertools
from functools import lru_cache
from typing import List

from tensorflow import keras

from src.modelisation.modelisation import Cube

NUMBER_OF_INPUTS = 6 * 9


def retrieve_possible_outputs(n) -> List[List[str]]:
    cube = Cube(3)

    combinations = []
    all_combinations = []
    # Create all possible combinations of moves using the itertools module
    for i in range(1, n + 1):
        moves_combinations = list(itertools.product(cube.perms, repeat=i))
        all_combinations.extend(moves_combinations)

        if i % 2 == 0:
            good_combinations = []

            for index, combination in enumerate(map(list, moves_combinations)):
                new_cubex = cube.permute(combination)
                if new_cubex.cube != cube.cube.tolist():
                    good_combinations.append(combination)

            moves_combinations = good_combinations

        combinations.extend(moves_combinations)

    return combinations


def create_model(n) -> keras.Model:
    possible_outputs = retrieve_possible_outputs(n)
    possible_outputs = list(map(lambda x: " ".join(x), possible_outputs))

    inputs = keras.Input(shape=(NUMBER_OF_INPUTS,))
    x = keras.layers.Dense(128, activation="relu")(inputs)
    x = keras.layers.Dense(128, activation="relu")(x)
    outputs = keras.layers.Dense(len(possible_outputs), activation="softmax")(x)

    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss=keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    return model


model = create_model(3)

model.summary()

