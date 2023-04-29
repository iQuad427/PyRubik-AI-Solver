import heapq
import math

from src.modelisation.modelisation import Cube, final_position
from src.search.evaluation.entropy import entropy_based_score_evaluation_function
from src.search.evaluation.look_up.functions.distances import simple_distances_total_independent_moves_all_3x3, \
    simple_distances_total_independent_moves_all_2x2
from src.search.models.game_state import GameState


def dijkstra_search(model: Cube, queue=None):
    if model.n == 2:
        heuristic = simple_distances_total_independent_moves_all_2x2
    elif model.n == 3:
        heuristic = simple_distances_total_independent_moves_all_3x3
    else:
        heuristic = entropy_based_score_evaluation_function

    best_score = math.inf
    print("best:", best_score)
    distances = {str(model.cube): 0}

    heap = [(best_score, model.cube, [])]
    heapq.heapify(heap)

    while len(heap) != 0:
        current = heapq.heappop(heap)
        # print(current)

        if current[0] < best_score:
            best_score = current[0]
            print(f"best score yet ({len(current[2])} moves):", current[0])
            print(current[2])
            print(model.permute(current[2]))

            if queue is not None:
                data = ""
                for move in current[2]:
                    data += f" {move}"
                queue.put(data)

        if final_position(current[1]):
            print("Solution Found")
            print("movements count:", len(current[2]))
            print("moves:", current[2])
            print(Cube(model.n, inner=current[1]))

            queue.put('quit')

            return current[2]

        for move in model.perms:
            distance = distances[str(current[1])] + 1
            next_state = Cube(model.n, inner=current[1]).permute([move])

            hashable = str(next_state.cube)

            if hashable not in distances or distances[hashable] > distance:
                heapq.heappush(heap, ((distance + 1) ** 2 * heuristic(GameState(next_state)), next_state.cube, current[2] + [move]))
                distances[hashable] = distance


if __name__ == '__main__':
    cube = Cube(3)
    scramble = cube.scramble(20)
    print(scramble)
    print(cube)

    dijkstra_search(cube)

    print(scramble)




