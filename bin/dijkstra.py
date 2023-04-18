from queue import Queue, PriorityQueue

from src.modelisation.modelisation import Cube
from src.search.evaluation.look_up.functions.distances import simple_distances_total_independent_moves_all_3x3
from src.search.models.game_state import GameState


def dijkstra_search(model: Cube, max_depth: int):
    queue = PriorityQueue()
    queue.put((0, model, []))

    while queue.qsize() != 0:
        current = queue.get()

        if simple_distances_total_independent_moves_all_3x3(GameState(current[1])) == 0:
            print(current)
            return current

        if current[0] < max_depth:
            for move in model.perms:
                queue.put((current[0] + 1, current[1].permute([move]), current[2] + [move]))
