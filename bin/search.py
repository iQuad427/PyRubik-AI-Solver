import math

from src.modelisation.modelisation import Cube
from src.evaluation.look_up.functions.distances import (
    simple_distances_total_independent_moves_3x3,
    simple_distances_total_independent_moves_all_3x3,
)
from src.search.models.game_state import GameState
from src.search.uninformed.depth import DepthFirstSearchEngine


def solve_using_standard_heuristic(cube):
    previous_best_score = math.inf

    while True:
        engine = DepthFirstSearchEngine(
            GameState(cube), simple_distances_total_independent_moves_3x3, 4
        )

        engine.run()

        # If a solution is found, update the number of solved cubes for the corresponding scramble level
        best_score = min(engine.best_scores)

        cube = engine.best_founds[engine.best_scores.index(best_score)].cube
        print("S: Best score: " + str(best_score))

        if best_score < previous_best_score:
            print(
                "S: New best score: " + str(best_score),
                "Previous: " + str(previous_best_score),
            )
            previous_best_score = best_score
        else:
            return cube, previous_best_score

        if best_score == 0:
            print("Solved using standard heuristic")


def solve_using_total_standard_heuristic(cube):
    previous_best_score = math.inf

    while True:
        engine = DepthFirstSearchEngine(
            GameState(cube), simple_distances_total_independent_moves_all_3x3, 4
        )

        engine.run()

        # If a solution is found, update the number of solved cubes for the corresponding scramble level
        best_score = min(engine.best_scores)

        cube = engine.best_founds[engine.best_scores.index(best_score)].cube
        print("R: Best score: " + str(best_score))

        if best_score < previous_best_score:
            print(
                "R: New best score: " + str(best_score),
                "Previous: " + str(previous_best_score),
            )
            previous_best_score = best_score
        else:
            return cube, previous_best_score

        if best_score == 8:
            print(cube)
            print("Solved using standard heuristic")


def solve_using_deep_and_standard_when_blocked(cube):
    previous_best_score = math.inf
    previous_heuristic_score = math.inf
    while True:
        engine = DepthFirstSearchEngine(
            GameState(cube), simple_distances_total_independent_moves_all_3x3, 3
        )
        engine.run()

        # If a solution is found, update the number of solved cubes for the corresponding scramble level
        best_score = min(engine.best_scores)

        cube = engine.best_founds[engine.best_scores.index(best_score)].cube

        if best_score < previous_best_score:
            print("New best score: " + str(best_score))
            previous_best_score = best_score
        else:
            print("Launching standard heuristic")
            cube, heur_score = solve_using_standard_heuristic(cube)
            if heur_score < previous_heuristic_score:
                previous_heuristic_score = heur_score
            else:
                cube, heur_score = solve_using_total_standard_heuristic(cube)
                previous_heuristic_score = math.inf

            previous_best_score = math.inf

        if best_score < 50:
            print("Solved")
            break

    print("Final cube:")
    print(cube)


cube = Cube(3)
cube.scramble(15)
print("Initial cube:")
print(cube)
# Search for a solution
beginner_moves = ["U", "D", "R", "L", "F", "B"]

solve_using_deep_and_standard_when_blocked(cube)
