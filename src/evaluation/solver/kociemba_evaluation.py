from src.modelisation.modelisation import Cube
from src.search.models.game_state import GameState
from src.modelisation.data import face_letter_color
import kociemba


def kociemba_distance_evaluation(state: GameState):
    cube_str = ""

    order = [0, 3, 2, 5, 1, 4]
    for i in order:
        face = state.cube.get_face_colors(i)
        for facet in face:
            cube_str += face_letter_color[facet]

    solve = kociemba.solve(cube_str).split(" ")
    length = sum([2 if len(move) == 2 and move[1] == "2" else 1 for move in solve])

    return 0 if state.cube else length


if __name__ == '__main__':
    cube = Cube(3)
    cube = cube.permute(['R', 'L', "B'", "F'", "L'", 'D', 'L', 'U', 'R', "L'", "F'", "U'", 'L', "B'", "L'", 'U', 'B', 'D', 'U', "B'", "B'", "R'", "B'", "U'", 'L', "F'", 'B', 'B', 'F', 'D'])
    moves = ['R', 'L', 'F', 'L', 'D', "F'", "R'", "U'", "D'", "L'", 'F', "U'", 'F', 'F', 'R', 'R', 'D', 'B', 'B', 'D', 'L', 'L', 'D', 'D', 'R', 'R', 'F', 'F']

    print(kociemba_distance_evaluation(GameState(cube)))
    for move in moves:
        cube = cube.permute([move])
        print(cube)
        print(kociemba_distance_evaluation(GameState(cube)))
