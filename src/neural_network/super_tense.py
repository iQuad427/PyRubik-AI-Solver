import itertools
import random
from typing import List

import numpy as np
from tensorflow import keras

from src.modelisation.modelisation import Cube

NUMBER_OF_INPUTS = 6 * 9 * 6


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
    x = keras.layers.Dense(256, activation="sigmoid")(inputs)
    x = keras.layers.Dense(256, activation="sigmoid")(x)
    outputs = keras.layers.Dense(len(possible_outputs), activation="softmax")(x)

    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss=keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    return model


x_data = []


def invert_moves(moves):
    inverted_moves = list(
        map(lambda x: x.replace("'", "") if "'" in x else f"{x}'", reversed(moves))
    )

    return inverted_moves


number_of_trainings = 100
number_of_steps_ahead = 1

trainings_inputs = []
trainings_outputs = []

all_possible_outputs = list(
    map(list, retrieve_possible_outputs(number_of_steps_ahead, number_of_steps_ahead))
)

moves = retrieve_possible_outputs(number_of_steps_ahead)

model = create_model(number_of_steps_ahead)

model.summary()

print(moves)

print(len(moves))


def get_cube_data_input(cube: Cube):
    data = cube.int_list()
    input_data = []

    for element in data:
        a = list(np.zeros(6))
        a[element] = 1
        input_data.extend(a)

    return input_data


for i in range(number_of_trainings + 100):
    cube = Cube(3)
    permutations = cube.scramble(random.randint(3, 20))
    inverted_permutations = invert_moves(permutations)[:number_of_steps_ahead]
    cube_data = get_cube_data_input(cube)
    trainings_inputs.append(cube_data)
    a = list(np.zeros(len(all_possible_outputs)))
    a[all_possible_outputs.index(inverted_permutations)] = 1
    trainings_outputs.append(a)

print("Training...")
model.fit(
    trainings_inputs[:number_of_trainings],
    trainings_outputs[:number_of_trainings],
    epochs=500,
)

a = 0

for i in range(10):
    x = model.predict(
        trainings_inputs[number_of_trainings : number_of_trainings + i + 1]
    )

    actual_response = all_possible_outputs[
        (trainings_outputs[number_of_trainings]).index(1)
    ]
    possibles = []
    print(f"Actual response: {actual_response}", end=" ")
    for prob in sorted(x[i], reverse=True)[:6]:
        move_index = list(x[i]).index(prob)
        ai_response = all_possible_outputs[move_index]
        possibles.append(ai_response)
        print("{:.2f}%: {}".format(prob * 100, ai_response), end=" ")
    print(actual_response in possibles)

    if actual_response in possibles:
        a += 1

print(f"Score: {a}/100")
