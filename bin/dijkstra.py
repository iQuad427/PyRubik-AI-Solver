import heapq
import multiprocessing
import time
from queue import Queue, PriorityQueue

from src.modelisation.modelisation import Cube, final_position
from src.search.evaluation.look_up.functions.distances import simple_distances_total_independent_moves_all_3x3
from src.search.models.game_state import GameState


def dijkstra_search(model: Cube, queue=None):
    heuristic = simple_distances_total_independent_moves_all_3x3

    best_score = heuristic(GameState(model))
    distances = {str(model.cube): 0}

    # Your search:
    heap = [(best_score, model.cube, [])]
    heapq.heapify(heap)

    while len(heap) != 0:
        current = heapq.heappop(heap)

        if current[0] < best_score:
            best_score = current[0]
            print("best score yet:", current[0])
            print(current[2])
            print(model.permute(current[2]))

            if queue is not None:
                data = ""
                for move in current[2]:
                    data += f" {move}"
                queue.put(data)

        if final_position(current[1]):
            print("Solution Found")
            print("movements count:", distances[str(current[1])])
            print("moves:", current[2])
            print(Cube(3, inner=current[1]))

            queue.put('quit')

            return current[2]

        for move in model.perms:
            distance = distances[str(current[1])] + 1
            next_state = Cube(3, inner=current[1]).permute([move])

            hashable = str(next_state.cube)

            if hashable not in distances or distances[hashable] > distance:
                heapq.heappush(heap, ((distance + 1) ** 3 * heuristic(GameState(next_state)), next_state.cube, current[2] + [move]))
                distances[hashable] = distance


if __name__ == '__main__':
    cube = Cube(3)
    scramble = cube.scramble(20)
    print(scramble)
    print(cube)

    dijkstra_search(cube)

    print(scramble)




