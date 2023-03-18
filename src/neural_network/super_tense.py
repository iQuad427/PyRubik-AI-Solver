import itertools
import random
from typing import List

import numpy as np
from tensorflow import keras

from src.modelisation.modelisation import Cube

NUMBER_OF_INPUTS = 6 * 9


def retrieve_possible_outputs(n, min_n=1) -> List[List[str]]:
    cube = Cube(3)

    combinations = []
    all_combinations = []
    # Create all possible combinations of moves using the itertools module
    for i in range(min_n, n + 1):
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
    possible_outputs = retrieve_possible_outputs(n, n)
    possible_outputs = list(map(lambda x: " ".join(x), possible_outputs))

    inputs = keras.Input(shape=(NUMBER_OF_INPUTS,))
    x = keras.layers.Dense(256, activation="relu")(inputs)
    x = keras.layers.Dense(256, activation="relu")(x)
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

x_data = []

moves = retrieve_possible_outputs(3)


def invert_moves(moves):
    inverted_moves = list(
        map(lambda x: x.replace("'", "") if "'" in x else f"{x}'", reversed(moves))
    )

    return inverted_moves


trainings_inputs = []
trainings_outputs = []

all_possible_outputs = list(map(list, retrieve_possible_outputs(3, 3)))


for i in range(500):
    cube = Cube(3)
    if i == 499:
        permutations = ["R", "R'", "R"]
    else:
        permutations = cube.scramble(random.randint(3, 20))
    inverted_permutations = invert_moves(permutations)[:3]
    cube_data = cube.int_list()
    trainings_inputs.append(cube_data)
    a = list(np.zeros(len(all_possible_outputs)))
    a[all_possible_outputs.index(inverted_permutations)] = 1
    trainings_outputs.append(a)

print("Training...")
model.fit(trainings_inputs[:499], trainings_outputs[:499], epochs=1000)

x = model.predict(trainings_inputs[499:500])
best_prob = max(x[0])
print(best_prob)
move_index = list(x[0]).index(best_prob)
print(move_index)
print(all_possible_outputs[move_index])
print(all_possible_outputs[(trainings_outputs[499]).index(1)])
