from src.modelisation.modelisation import Cube
from data import COLORS, resolved_cube, corners, edges


def invert_moves(moves):
    inverted_moves = list(
        map(lambda x: x.replace("'", "") if "'" in x else f"{x}'", reversed(moves))
    )

    return inverted_moves


def generate_inverse_moves(moves_dict):
    inverted_moves = {}
    for move in moves_dict:
        inverted_moves[f"{move}'"] = invert_permutation(moves_dict[move])

    return inverted_moves


def invert_permutation(lst):
    return [tuple(reversed(t)) for t in reversed(lst)]


def final_position(pos):
    """
    Verify if the position corresponds to a solution

    :param pos: the current position to test
    :return: whether the position is a solution or not

    # Inspiration: https://my.numworks.com/python/schraf/rubik
    """
    color, nb = pos[0], 1
    for facet in pos:
        if facet != color:
            color = facet
            nb += 1
    return nb == len(
        COLORS
    )  # we check if the number of color changes corresponds to the number of colors


def define_permutation(moves: list[tuple[int, ...]]):
    """
    Simplify the permutation associated to a list of basic permutations
    :param moves: list of permutation

    use: define_permutation([perms[move] for move in moves])
            where:  perms is the dict of moves -> permutation
                    moves is the list of movements (U, F, D, R, L, B)
    """
    fake_cube = [i for i in range(54)]
    apply_permutation(fake_cube, moves)

    return fake_cube


def apply_permutation(num: list[int], perm: list[tuple[int, ...]]):
    save = list(num)
    for t in perm:
        u = (t[-1],) + t
        for i, v in enumerate(t):
            num[v] = save[u[i]]


def face_is_complete(face: int, cube: Cube):
    colors = cube.get_face_colors(face)
    for color in colors:
        if color != colors[0]:
            return False

    return True


def verify_corner(corner: int, cube: Cube):
    return [resolved_cube[facet] for facet in corners[corner]] == [cube.cube[facet] for facet in corners[corner]]


def verify_edge(edge: int, cube: Cube):
    return [resolved_cube[facet] for facet in edges[edge]] == [cube.cube[facet] for facet in edges[edge]]


def compute_distance_to_position(piece: int, cube: Cube):
    # TODO: implement (need to differentiate corners and edges, either two function or parameter)
    pass

# TODO: implement breadth first to compute the lowest possible number of moves to put the piece at the right position
#  using basic moves from perm dictionary of the cube
