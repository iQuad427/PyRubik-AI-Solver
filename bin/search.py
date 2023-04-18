import math
import random

import matplotlib.pyplot as plt

from src.modelisation.modelisation import Cube
from src.neural_network.ai_heuristic.super import deep_learning_evaluate_function
from src.search.evaluation.look_up.functions.distances import (
    simple_distances_total_independent_moves_all_3x3,
)
from src.search.evaluation.membership import face_color_membership_evaluation_function
from src.search.models.game_state import GameState
from src.search.uninformed.depth import DepthFirstSearchEngine

# Define the number of cubes to solve
NUM_CUBES = 20
# Define the maximum depth for the search
MAX_DEPTH = 4

MAX_SCRAMBLES = 20


# Initialize variables to keep track of the number of solved cubes
num_solved = [0] * (MAX_SCRAMBLES - 4)
num_trials = [0] * (MAX_SCRAMBLES - 4)

for i in range(NUM_CUBES):
    # Initialize the Rubik's Cube and scramble it between 5 and 15 moves
    cube = Cube(3)
    num_scrambles = random.randint(5, MAX_SCRAMBLES)
    num_trials[num_scrambles - 5] += 1
    cube.scramble(num_scrambles)

    # Initialize the search engine
    eval_func_rotations = [
        deep_learning_evaluate_function,
    ]
    x = 0
    previous_best_score = math.inf
    depth = 2

    print(
        "Initial evaluation: " + str(deep_learning_evaluate_function(GameState(cube)))
    )

    # Search for a solution
    while True:
        eval_func = eval_func_rotations[x % len(eval_func_rotations)]
        engine = DepthFirstSearchEngine(GameState(cube), eval_func, depth)
        result = engine.run()

        # If a solution is found, update the number of solved cubes for the corresponding scramble level
        best_score = min(engine.best_scores)
        if best_score == 1:
            num_solved[num_scrambles - 5] += 1
            break

        # Adjust the depth of the search if there is no improvement
        if previous_best_score == best_score:
            depth += 1
            if depth > MAX_DEPTH:
                break
        else:
            depth = 2
            previous_best_score = best_score

        cube = engine.best_founds[engine.best_scores.index(best_score)].cube
        x += 1

# Display the number of solved cubes per scramble level in percentage
plt.bar(
    [i for i in range(5, MAX_SCRAMBLES)],
    [
        (num_solved[i] / num_trials[i]) * 100 if num_trials[i] else 1
        for i in range(MAX_SCRAMBLES - 5)
    ],
    color="blue",
)
plt.xlabel("Number of scrambles")
plt.ylabel("Percentage of solved cubes")
plt.show()
