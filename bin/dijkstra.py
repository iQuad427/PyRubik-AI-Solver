import heapq
from queue import Queue, PriorityQueue

from src.modelisation.modelisation import Cube, final_position, simplify_list_of_perms
from src.search.evaluation.look_up.functions.distances import simple_distances_total_independent_moves_all_3x3
from src.search.models.game_state import GameState


def dijkstra_search(model: Cube, max_depth: int):
    heuristic = simple_distances_total_independent_moves_all_3x3
    distances = {model.cube: 0}

    # Your search:
    heap = [(0, model.cube, [])]
    heapq.heapify(heap)

    while len(heap) != 0:
        current = heapq.heappop(heap)
        print(current[2])

        if final_position(current[1]):
            print("Solution Found")
            break

        for move in model.perms:
            distance = distances[current[1]] + 1
            next_state = model.permute([move])

            if next_state.cube not in distances or distances[next_state] > distance:
                heapq.heappush(heap, (heuristic(GameState(Cube(3, inner=next_state))), next_state, current[2] + [move]))
                distances[next_state] = distance


if __name__ == '__main__':
    cube = Cube(3)
    scramble = cube.scramble(30)
    print(scramble)
    print(simplify_list_of_perms(scramble))
