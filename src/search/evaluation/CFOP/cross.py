from src.modelisation.data import EDGES_PER_FACE
from src.modelisation.modelisation import Cube, verify_edge
from src.search.models.game_state import GameState
from src.search.uninformed.iterative_depth import IterativeDeepeningSearchEngine


def white_cross_evaluation(state: GameState):
    score = 0

    for edge in range(EDGES_PER_FACE):  # we consider only the white cross pieces (4 first edges)
        if not verify_edge(edge, state.cube):  # if edge is well-placed, no negative impact
            score += 1

    return score


if __name__ == '__main__':
    cube = Cube(3)
    # cube.scramble(10)
    print(cube)

    game = GameState(cube)
    print(white_cross_evaluation(game))

