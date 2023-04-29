from queue import Queue

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

import src.modelisation.modelisation as model
from src.animation.cube_interactive import Cube, CubeAnimation
from src.search.dijkstra.dijkstra import dijkstra_search
from multiprocessing import Queue, Process

from src.search.evaluation.look_up.functions.distances import simple_distances_total_independent_moves_all_3x3
from src.search.models.game_state import GameState

if __name__ == '__main__':
    q = Queue()
    model = model.Cube(3)
    scramble = model.scramble(20)
    print("Scramble:", scramble)
    print(model)

    p = Process(target=dijkstra_search, args=(model, q))
    p.start()

    c = Cube(3)
    figure, axe = c.draw_interactive()
    figure.add_axes(axe)
    axe.update_cube(scramble, [])

    animation = FuncAnimation(figure, CubeAnimation.animate, frames=100, fargs=(axe, p, q, scramble))

    plt.show()
