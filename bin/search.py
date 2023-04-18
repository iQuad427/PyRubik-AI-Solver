import math
import random

from src.modelisation.modelisation import Cube
from src.neural_network.ai_heuristic.super import (
    deep_learning_evaluate_function,
    evaluate_cube,
)
from src.search.evaluation.membership import face_color_membership_evaluation_function
from src.search.models.game_state import GameState
from src.search.uninformed.depth import DepthFirstSearchEngine

if __name__ == "__main__":
    cube = Cube(3)
    cube.scramble(15)
    print(cube)
    print("Normal eval", face_color_membership_evaluation_function(GameState(cube)))

    # cleanup cube with

    eval_func_rotations = [
        deep_learning_evaluate_function,
        deep_learning_evaluate_function,
        deep_learning_evaluate_function,
        deep_learning_evaluate_function,
    ]

    depth_rotation = [3, 3, 3, 3]

    x = 0

    previous_best_score = math.inf

    previous_best = set()

    while True:
        eval_func = eval_func_rotations[x % len(eval_func_rotations)]
        engine = DepthFirstSearchEngine(
            GameState(cube), eval_func, depth_rotation[x % len(depth_rotation)]
        )
        result = engine.run()

        best_found_score_excluding_previous = [
            found for found in engine.best_scores if found not in previous_best
        ]

        if not best_found_score_excluding_previous:
            print("No new best found")
            break

        if len(previous_best) > 10:
            print("Clearing previous best")
            previous_best = set()


        best_score = min(best_found_score_excluding_previous)
        best_found = engine.best_founds[engine.best_scores.index(best_score)]

        previous_best.add(best_score)

        print("New best score:", best_score)
        print("New best found:", best_found.cube)

        print(best_score)

        if best_score == 1:
            print(cube)
            print("Solved!")
            break
        cube = best_found.cube
        x += 1
