from multiprocessing import Process, Queue

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

import src.modelisation.modelisation as model
from src.animation.cube_interactive import Cube, CubeAnimation
from src.evaluation.look_up.functions.distances import simple_distances_total_independent_moves_all_3x3
from src.search.dijkstra.dijkstra import dijkstra_search

if __name__ == "__main__":
    size = 3

    q = Queue()
    model = model.Cube(size)
    scramble = model.scramble(15)
    print("Scramble:", scramble)
    print(model)

    p = Process(target=dijkstra_search, args=(model, q, simple_distances_total_independent_moves_all_3x3))
    p.start()

    c = Cube(size)
    figure, axe = c.draw_interactive()
    figure.add_axes(axe)
    axe.update_cube(scramble, [])

    animation = FuncAnimation(
        figure, CubeAnimation.animate, frames=100, fargs=(axe, p, q, scramble)
    )

    plt.show()
