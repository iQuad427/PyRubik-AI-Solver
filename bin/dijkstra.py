import heapq
from queue import Queue, PriorityQueue

from src.modelisation.modelisation import Cube, final_position, simplify_list_of_perms
from src.search.evaluation.entropy import translated_entropy_based_score_evaluation_function
from src.search.evaluation.look_up.functions.distances import simple_distances_total_independent_moves_all_3x3
from src.search.models.game_state import GameState


def dijkstra_search(model: Cube, max_depth: int):
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

        if final_position(current[1]):
            print("Solution Found")
            print("movements count:", distances[str(current[1])])
            print("moves:", current[2])
            print(Cube(3, inner=current[1]))
            return current[2]

        for move in model.perms:
            distance = distances[str(current[1])] + 1
            next_state = Cube(3, inner=current[1]).permute([move])

            hashable = str(next_state.cube)

            if hashable not in distances or distances[hashable] > distance:
                heapq.heappush(heap, ((distance + 1) * heuristic(GameState(next_state)), next_state.cube, current[2] + [move]))
                distances[hashable] = distance


if __name__ == '__main__':
    cube = Cube(3)
    scramble = cube.scramble(15)
    print(scramble)
    print(cube)

    dijkstra_search(cube, 20)

    print(scramble)




