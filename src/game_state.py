import math
import queue
import random
from typing import Callable

from src.modelisation.modelisation import Cube


class GameState:
    moves = ["U", "R", "F", "L", "B", "D"]

    def __init__(self, cube: Cube, depth: int = 0):
        self.cube = cube
        self.depth = depth

    def get_legal_actions(self):
        return self.cube.perms

    def generate_successor(self, action):
        return GameState(
            self.cube.permute(action),
            self.depth + 1
        )


def score_evaluation(state: GameState):
    totat_score = 0

    for i in range(state.cube.n):
        colors = state.cube.get_face_colors(i)

        # Entropy as n*log(n,2) of number of colors on a face
        num_colors = len(set(colors))
        entropy = num_colors * math.log(num_colors, 2)

        totat_score += entropy

    return totat_score


class GameEngine:
    def __init__(self, starting_state: GameState, evaluation_function: Callable[[GameState], int], max_depth=math.inf):
        self.state = starting_state
        self.evaluation_function = evaluation_function
        self.max_depth = max_depth

    def run(self):
        container = [self.state]

        while container:
            # Remove previous print
            state = container.pop(0)
            print(state.depth)
            if self.evaluation_function(state) == 0:
                return state

            for action in state.get_legal_actions():
                if state.depth < self.max_depth:
                    container.insert(0, state.generate_successor(action))

        return None


if __name__ == '__main__':
    initial_state = GameState(Cube(3))

    random.shuffle(initial_state.cube.cube)

    engine = GameEngine(initial_state, score_evaluation, max_depth=3)

    solution = engine.run()

    print(solution)
    print(solution.cube if solution else "No solution found")
