import json
from collections import defaultdict

from src.modelisation.modelisation import Cube
from src.search.evaluation.CFOP.cross import white_cross_evaluation
from src.search.evaluation.distance import distance_to_good_face_evaluation_function
from src.search.evaluation.entropy import entropy_based_score_evaluation_function, \
    translated_entropy_based_score_evaluation_function
from src.search.evaluation.look_up.functions.distances import simple_distances_total_independent_moves_3x3, \
    simple_distances_total_independent_moves_2x2, simple_distances_total_independent_moves_all_3x3
from src.search.evaluation.membership import face_color_membership_evaluation_function
from src.search.informed.a_star import AStarSearchEngine
from src.search.informed.step_by_step_a_star import AStarStepByStep
from src.search.models.game_state import GameState
from src.search.stochastic.iterative import IteratedLocalSearch
from src.search.uninformed.breadth import BreadthFirstSearchEngine
from src.search.uninformed.iterative_depth import IterativeDeepeningSearchEngine


def time_function(function, *args, **kwargs):
    import time

    start = time.time()
    result = function(*args, **kwargs).run()
    print(result)
    if not result:
        return -1

    end = time.time()
    return end - start


if __name__ == "2__main__":
    cube = Cube(3)
    cube.scramble(20)

    print(cube)

    def combined_evaluation_function(state: GameState):
        return (
            distance_to_good_face_evaluation_function(state)
            + 0.3 * entropy_based_score_evaluation_function(state)
            + 0.3 * face_color_membership_evaluation_function(state)
        )

    print(combined_evaluation_function(GameState(cube)))

    result = AStarStepByStep(GameState(cube), combined_evaluation_function, 100)

    result.run()
    print(combined_evaluation_function(result.state))
    print(result.state.cube)


# if __name__ == "__main__":
#
#     engines = [
#         # IteratedLocalSearch,
#         # FirstImprovement,
#         # BestImprovement,
#         # AStarSearchEngine,
#         IterativeDeepeningSearchEngine,
#         # DepthFirstSearchEngine,
#         # IterativeDeepeningAStarSearchEngine,
#         # AStarStepByStep,
#         # BreadthFirstSearchEngine,
#     ]
#
#     data = defaultdict(list)
#
#     for engine in engines:
#         for i in range(1, 10):
#             total_for_this_config = 0
#             for _ in range(1):
#                 cube = Cube(3)
#                 cube.scramble(i)
#                 time = time_function(
#                     engine,
#                     GameState(cube),
#                     simple_distances_total_independent_moves_all_3x3,
#                     max_depth=7,
#                 )
#                 total_for_this_config += time
#
#             data[str(engine)].append(total_for_this_config / 10)
#             print("=====================================")
#             print(json.dumps(data, indent=4))
#
#     print(data)

if __name__ == '__main__':
    cube = Cube(3)
    scramble = cube.scramble(150)
    print(scramble)
    print(cube)

    engine = AStarSearchEngine(
        GameState(cube),
        simple_distances_total_independent_moves_all_3x3
    )

    solution = engine.run()

    print(solution)

