import heapq
import math

from src.evaluation.solver.kociemba_evaluation import kociemba_distance_evaluation
from src.modelisation.data import scrambled_3, scrambled_2
from src.modelisation.modelisation import Cube, final_position
from src.search.models.game_state import GameState


def dijkstra_search(model: Cube, queue=None, evaluation_function=None, distance=True):
    best_score = math.inf
    number_move = 0
    distances = {str(model.cube): 0}

    heap = [(best_score, model.cube, [])]
    heapq.heapify(heap)

    weight = evaluation_function(GameState(Cube(model.n, inner=eval(f"scrambled_{model.n}"))))

    # Use the heuristic typical value to extend the weight to give to the distance
    # (Used to avoid giving too much importance to the distance and inversely)
    if weight < 1:
        distance_weighting = lambda x: 1
        distance_heuristic_link = lambda x, y: x * y
    elif weight < 1_000:
        distance_weighting = lambda x: 2 * x if distance else 0
        distance_heuristic_link = lambda x, y: x + y
    elif weight < 100_000:
        distance_weighting = lambda x: 10 * x if distance else 0
        distance_heuristic_link = lambda x, y: x + y
    elif weight < 1_000_000:
        distance_weighting = lambda x: x if distance else 1
        distance_heuristic_link = lambda x, y: x * y
    else:
        distance_weighting = lambda x: (1 + x) ** 2 if distance else 1
        distance_heuristic_link = lambda x, y: x * y

    while len(heap) != 0:
        current = heapq.heappop(heap)
        # print(current)

        if current[0] < best_score or (current[0] == best_score and len(current[2]) < number_move):
            best_score = current[0]
            print(f"best score yet ({len(current[2])} moves):", current[0])
            print(current[2])
            print(model.permute(current[2]))

            number_move = len(current[2])

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

            queue.put("quit")

            return current[2]

        for move in model.perms:
            distance = distances[str(current[1])] + 1
            next_state = Cube(model.n, inner=current[1]).permute([move])

            hashable = str(next_state.cube)

            if hashable not in distances or distances[hashable] > distance:
                heapq.heappush(
                    heap,
                    (
                        distance_heuristic_link(
                            distance_weighting(distance),
                            evaluation_function(GameState(next_state))
                        ),
                        next_state.cube,
                        current[2] + [move],
                    ),
                )
                distances[hashable] = distance

