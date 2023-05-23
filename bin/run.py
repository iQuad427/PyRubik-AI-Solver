from multiprocessing import Process, Queue

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

import src.modelisation.modelisation as model
from src.animation.cube_interactive import Cube, CubeAnimation
from src.evaluation.basic.combined import combined_simple_heuristics_evaluation, \
    combined_simple_heuristics_evaluation_upscaled, combines_simple_heuristics_evaluation_2x2
from src.evaluation.basic.distance import distance_to_good_face_evaluation_function
from src.evaluation.basic.entropy import entropy_based_score_evaluation_function
from src.evaluation.basic.membership import face_color_membership_evaluation_function
from src.evaluation.look_up.functions.distances import simple_distances_total_independent_moves_all_3x3, \
    simple_distances_total_independent_moves_all_3x3_upscaled, simple_distances_total_independent_moves_3x3, \
    simple_distances_total_independent_moves_all_2x2, simple_distances_total_independent_moves_all_2x2_upscaled
from src.evaluation.ml.gradient_booster_regressor import gbr_regressor_evaluation_function
from src.evaluation.ml.neural_network_regressor import nnr_regressor_evaluation_function
from src.evaluation.ml.support_vector_regression import svr_regressor_evaluation_function
from src.evaluation.solver.kociemba_evaluation import kociemba_distance_evaluation
from src.search.dijkstra.dijkstra import dijkstra_search

if __name__ == "__main__":
    # PARAMETERS
    cube_size = 3  # only supports 2 or 3 for now
    scramble_size = 25
    # the heuristic used should be compatible with the size given above
    evaluation_function = kociemba_distance_evaluation
    size_is_importance = True
    automatic_scaling = False
    moves_objective = 25  # only considered if automatic_scaling

    # Create the cube and scramble it
    model = model.Cube(cube_size)
    scramble = model.scramble(scramble_size)
    print("Scramble:", scramble)
    print(model)

    # Run A* on the given scramble
    q = Queue()  # for inter-process communication with the visualisation from the solver
    p = Process(
        target=dijkstra_search,
        args=(model, q,
              evaluation_function,
              size_is_importance,
              automatic_scaling,
              moves_objective
              )
    )
    p.start()

    # Showcase the cube resolution
    c = Cube(cube_size)
    figure, axe = c.draw_interactive()
    figure.add_axes(axe)
    axe.update_cube(scramble, [])

    animation = FuncAnimation(
        figure, CubeAnimation.animate, frames=100, fargs=(axe, p, q, scramble)
    )

    plt.show()
