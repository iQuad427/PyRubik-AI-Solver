import random
from typing import List
import numpy as np

from src.modelisation.data import colors, n, moves, edges, COLORS, corners_3x3, resolved_cube_3x3


class Cube:
    def __init__(self, dim, inner=None):
        self.n = dim

        if inner is not None:
            self.cube = inner
        else:
            self.cube = self._generate_cube()

        self.perms = generate_lateral_moves(self.n)
        self.perms.update(generate_crown_moves(self.n))
        # self.perms.update(generate_double_moves(self.perms))
        self.perms.update(generate_inverse_moves(self.perms))
        self.perms["N"] = None

    def __bool__(self):
        return final_position(self.cube)

    def __str__(self):
        if self.n == 3:
            return """
                            0----|----|----|
                            |  {0} |  {1} |  {2} |
                            |----|----|----|
                            |  {3} |  {4} |  {5} |
                            |----|----|----|
                            |  {6} |  {7} |  {8} |
                            |----|----|----|
            1----|----|----|2----|----|----|3----|----|----|4----|----|----|
            |  {9} |  {10} |  {11} ||  {18} |  {19} |  {20} ||  {27} |  {28} |  {29} ||  {36} |  {37} |  {38} |
            |----|----|----||----|----|----||----|----|----||----|----|----|
            |  {12} |  {13} |  {14} ||  {21} |  {22} |  {23} ||  {30} |  {31} |  {32} ||  {39} |  {40} |  {41} |
            |----|----|----||----|----|----||----|----|----||----|----|----|
            |  {15} |  {16} |  {17} ||  {24} |  {25} |  {26} ||  {33} |  {34} |  {35} ||  {42} |  {43} |  {44} |
            |----|----|----||----|----|----||----|----|----||----|----|----|
                            5----|----|----|
                            |  {45} |  {46} |  {47} |
                            |----|----|----|
                            |  {48} |  {49} |  {50} |
                            |----|----|----|
                            |  {51} |  {52} |  {53} |
                            |----|----|----|
            """.format(
                *[self.cube[i] for i in range(self.n * self.n * 6)]
            )
        elif self.n == 2:
            return """            
                           0----|----|  
                           |  {0} |  {1} |  
                           |----|----| 
                           |  {2} |  {3} | 
                           |----|----| 
                1----|----|2----|----|3----|----|4----|----|   
                |  {4} |  {5} ||  {8} |  {9} ||  {12} |  {13} ||  {16} |  {17} |   
                |----|----||----|----||----|----||----|----|   
                |  {6} |  {7} ||  {10} |  {11} ||  {14} |  {15} ||  {18} |  {19} |   
                |----|----||----|----||----|----||----|----|   
                           5----|----| 
                           |  {20} |  {21} | 
                           |----|----| 
                           |  {22} |  {23} | 
                           |----|----| 
                    """.format(
                *[self.cube[i] for i in range(self.n * self.n * 6)]
            )

    def _generate_cube(self):
        model = []
        for color in colors:
            for i in range(self.n * self.n):
                model.append(color)

        return np.array(model)

    def scramble(self, times: int):
        shuffle = random.choices(list(self.perms.keys()), k=times)
        self._permute(self.cube, shuffle)

        return shuffle

    def permute(self, perms: List[str]):
        """
        Apply a permutation to the current cube state

        :param perms: list of letters corresponding to the perm we want to apply
        :return: a new cube on which the permutations were applied

        Inspiration: https://my.numworks.com/python/schraf/rubik
        """

        new_cube = list(self.cube)

        self._permute(new_cube, perms)

        return Cube(self.n, new_cube)

    def _permute(self, new_cube, perms):
        for perm in perms:
            if perm != "N":
                save = list(new_cube)
                mvt = self.perms[perm]
                for t in mvt:
                    u = (t[-1],) + t
                    for i, v in enumerate(t):
                        new_cube[v] = save[u[i]]

    def get_face_colors(self, face: int) -> List[str]:
        return self.cube[face * self.n * self.n: (face + 1) * self.n * self.n - 1]

    def get_color(self, face: int, row: int, col: int) -> List[str]:
        return self.cube[face * self.n * self.n + row * self.n + col]

    def int_list(self):
        int_data = []

        for color in self.cube:
            int_data.append(colors.index(color))

        return int_data


def get_position_index(n: int, face: int, row: int, col: int):
    return n * n * face + n * row + col


def generate_crown_moves(n: int):
    # TODO : moving centers might be bad for the algorithms -> might keep only non-center crowns permutation
    permutations = {}

    # Transversal crown permutations
    for i in range(1, n - 1):
        if n % 2 == 0 or i != n // 2:
            permutation_m = []
            permutation_e = []
            permutation_s = []
            for j in range(n):
                # M - Transversal crown permutations - starts from face 1 (then 2, 3, 4)
                permutation_m.append(
                    (
                        get_position_index(n, 0, j, i),
                        get_position_index(n, 2, j, i),
                        get_position_index(n, 5, j, i),
                        get_position_index(n, 4, n - j - 1, n - i - 1),
                    )
                )

                # E - Sagittal crown permutations - starts from face 0 (then 2, 5, 4)
                permutation_e.append(
                    (
                        get_position_index(n, 1, i, j),
                        get_position_index(n, 2, i, j),
                        get_position_index(n, 3, i, j),
                        get_position_index(n, 4, i, j),
                    )
                )

                # S - Frontal crown permutation - starts from face 0 (then 3', 5, 1')
                permutation_s.append(
                    (
                        get_position_index(n, 0, i, j),
                        get_position_index(n, 3, j, i),
                        get_position_index(n, 5, n - i - 1, n - j - 1),
                        get_position_index(n, 1, n - j - 1, i),
                    )
                )

            permutations[f"{i}M"] = permutation_m
            permutations[f"{i}E"] = permutation_e
            permutations[f"{i}S"] = permutation_s

    return permutations


def generate_lateral_moves(n: int):
    permutations = {}

    for face, move in enumerate(moves):
        # corners permutation : 1
        permutation = [
            (
                get_position_index(n, face, 0, 0),
                get_position_index(n, face, 0, n - 1),
                get_position_index(n, face, n - 1, n - 1),
                get_position_index(n, face, n - 1, 0),
            )
        ]

        # edges permutations : n - 2 (from 1 to n - 1)
        for i in range(1, n):
            permutation.append(
                (
                    get_position_index(n, face, 0, i),
                    get_position_index(n, face, i, n - 1),
                    get_position_index(n, face, n - 1, n - i - 1),
                    get_position_index(n, face, n - i - 1, 0),
                )
            )

        # edges permutation : n
        if move == "U":
            for j in range(n):
                permutation.append(
                    (  # 0 : Up face - 4, 3, 2, 1
                        get_position_index(n, 4, 0, j),
                        get_position_index(n, 3, 0, j),
                        get_position_index(n, 2, 0, j),
                        get_position_index(n, 1, 0, j),
                    )
                )

        if move == "L":
            for j in range(n):
                permutation.append(
                    (  # 1 : Left face - 0, 2, 5, 4
                        get_position_index(n, 0, j, 0),
                        get_position_index(n, 2, j, 0),
                        get_position_index(n, 5, j, 0),
                        get_position_index(n, 4, n - j - 1, n - 1),
                    )
                )
        if move == "F":
            for j in range(n):
                permutation.append(
                    (  # 2 : Front face - 0, 3, 5, 1
                        get_position_index(n, 0, n - 1, j),
                        get_position_index(n, 3, j, 0),
                        get_position_index(n, 5, 0, n - j - 1),
                        get_position_index(n, 1, n - j - 1, n - 1),
                    )
                )

        if move == "R":
            for j in range(n):
                permutation.append(
                    (  # 3 : Right face - 5, 2, 0, 4
                        get_position_index(n, 5, j, n - 1),
                        get_position_index(n, 2, j, n - 1),
                        get_position_index(n, 0, j, n - 1),
                        get_position_index(n, 4, n - j - 1, 0),
                    )
                )

        if move == "B":
            for j in range(n):
                permutation.append(
                    (  # 4 : Back face - 0, 1, 5, 3
                        get_position_index(n, 0, 0, n - j - 1),
                        get_position_index(n, 1, j, 0),
                        get_position_index(n, 5, n - 1, j),
                        get_position_index(n, 3, n - j - 1, n - 1),
                    )
                )

        if move == "D":
            for j in range(n):
                permutation.append(
                    (  # 5 : Down face - 1, 2, 3, 4
                        get_position_index(n, 1, n - 1, j),
                        get_position_index(n, 2, n - 1, j),
                        get_position_index(n, 3, n - 1, j),
                        get_position_index(n, 4, n - 1, j),
                    )
                )

        permutations[move] = permutation

    return permutations


def generate_double_moves(perms: dict):
    permutation = {}
    for move in moves:
        permutation[f"{move}2"] = perms[move] * 2

    return permutation


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


def simplify_list_of_perms(perms: list[str]):
    """
    Method to simplify a list of moves

    :param perms: list of sequential move to perform
    :return: simplified list of move to do the same thing

    example :
        - previous : ['B', "B'", 'B', "D'", 'B', 'D', 'B', "B'", 'N', "D'", "F'", 'L', "R'", "D'", 'N', 'L', "F'", 'U', 'N', 'D', "F'", 'F', 'D', "D'", 'N', "L'", 'N', 'D', 'N', "D'"]
        - becomes : ['B', "D'", 'B', "F'", 'L', "R'", "D'", 'L', "F'", 'U', 'D', "L'"]
    """
    new_perms = []

    for perm in perms:
        print(perm)
        if perm == "N":
            continue

        if new_perms:
            top = new_perms[-1]
            print("top :", top)

            if top == perm + "'" or perm == top + "'":
                new_perms.pop()
                continue

        new_perms.append(perm)

    return new_perms


def permute_from_defined_permutation(cube: Cube, indexed_cube: list[int]):
    model = []
    for index in indexed_cube:
        model.append(cube.cube[index])

    return np.array(model)


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
    return [resolved_cube_3x3[facet] for facet in corners_3x3[corner]] == [cube.cube[facet] for facet in corners_3x3[corner]]


def verify_edge(edge: int, cube: Cube):
    return [resolved_cube_3x3[facet] for facet in edges[edge]] == [cube.cube[facet] for facet in edges[edge]]


def compute_distance_to_position(piece: int, cube: Cube):
    # TODO: implement (need to differentiate corners and edges, either two function or parameter)
    pass

# TODO: implement breadth first to compute the lowest possible number of moves to put the piece at the right position
#  using basic moves from perm dictionary of the cube


if __name__ == '__main__':
    test = ['F', 'R', 'L', "R'", "B'", 'L', 'B', "B'", "F'", "B'", "B'", "L'", 'N', "U'", 'D', "L'", "U'", 'N', 'L', 'B', 'N', "D'", "U'", "B'", "D'", 'R', "L'", "U'", "D'", 'U', 'D', "F'", "F'", 'B', 'U', "R'", 'L', 'F', "D'", "D'", 'U', 'B', "D'", "R'", 'R', "B'", "B'", "U'", 'D', "U'", 'U', 'F', 'L', 'R', "R'", 'F', 'R', 'U', "L'", 'L', 'F', "L'", 'F', 'U', 'N', 'B', 'R', 'D', 'D', 'R', 'R', "L'", 'B', 'F', "B'", "D'", 'R', "D'", "D'", 'N', 'N', "F'", "F'", 'D', 'L', "L'", 'D', "R'", 'D', "U'", 'U', "R'", 'D', "B'", 'U', 'L', 'F', "L'", "R'", "L'", 'U', "B'", "R'", 'U', 'F', 'L', "F'", "U'", "F'", 'D', "U'", "U'", "L'", "B'", "L'", "B'", "F'", "F'", "B'", 'B', "R'", "B'", "R'", 'R', 'R', "U'", "B'", 'B', 'D', "R'", "R'", 'U', "B'", 'N', 'N', 'F', "U'", 'R', "R'", 'F', 'B', 'L', "L'", 'F', "R'", "U'", 'U', 'L', "B'", "U'", 'N', "F'", 'N', "D'", 'N', "U'", 'F', 'U', 'D', "L'", "R'", "R'", "R'", 'F', "U'", "D'", 'N', "B'", "R'", 'R', "F'", "L'", "D'", "R'", 'U', "D'", "U'", "L'", "F'", 'F', 'N', 'F', "U'", "U'", "L'", "L'", "B'", 'N', "D'", 'L', 'U', "L'", 'F', 'U', 'B', "L'", "L'", 'N', 'F', 'B', "L'", 'D', 'R', "F'", "U'", 'F', "R'", 'D', "U'", "U'", 'N', 'F', "D'", "L'", "D'", 'R', "U'", "B'", 'D', 'L', 'D', "D'", "U'", "L'", "U'", "U'", 'D', "L'", "D'", "R'", "D'", 'R', 'L', 'D', "L'", 'F', 'U', 'U', "B'", 'B', 'U', 'U', "L'", 'F', 'D', "D'", "L'", 'N', "B'", "L'", "U'", "L'", 'U', "B'", 'D', 'N', "U'", 'L', 'U', 'L', "F'", 'N', 'R', "U'", "F'", 'F', "R'", 'L', 'D', 'U', 'F', 'D', "R'", "U'", 'D', "U'", "L'", 'L', 'D', "F'", 'N', 'R', 'N', 'R', "F'", 'D', 'L', 'D', 'F', "F'", "F'", 'L', 'U', "B'", 'B', 'L', 'F', 'N', "B'", "R'", 'F', "B'", 'U', 'L', "B'", "D'", "U'", 'R', 'U', "L'", "B'", 'U', 'B', 'U', "L'", 'L', "B'", "R'", 'N', 'U', "L'", "B'", 'L', "B'", "U'", "R'", 'B', 'D', 'F', "L'", 'N', 'U', 'F', 'L', "R'", 'U', 'D', 'L', 'N', "F'", 'U', 'F', 'N', "L'", 'L', 'F', 'F', "L'", "F'", 'F', 'L', "D'", "L'", 'D', "D'", "D'", 'N', 'R', 'F', 'B', 'F', "U'", "D'", 'N', "R'", "F'", "F'", "U'", 'L', "L'", 'B', 'L', 'B', "B'", "B'", "B'", 'L', 'B', 'B', "F'", 'U', 'F', "F'", "D'", 'N', 'D', 'F', "U'", "B'", "U'", "L'", "B'", "U'", 'D', "D'", "L'", 'R', 'U', "B'", 'U', "D'", 'U', "B'", 'L', "B'", 'D', "D'", "L'", "U'", "B'", 'F', 'U', 'U', 'N', "F'", 'U', 'R', "F'", 'B', 'R', 'B', "D'", 'U', 'N', "R'", 'U', 'L', 'U', 'F', "U'", 'L', 'L', 'F', "U'", "B'", "U'", 'B', 'B', 'L', "L'", 'D', 'N', 'N', 'L', 'R', 'U', 'L', "U'", "L'", "R'", 'L', "D'", "R'", "L'", "F'", 'L', 'B', "L'", "U'", 'R', "F'", 'L', "R'", 'F', 'F', 'D', "R'", 'F', 'U', "L'", "L'", 'D', 'R', 'D', "B'", 'R', "D'", "D'", "R'", "D'", 'B', 'R', 'L', 'F', 'F', "U'", 'F', 'N', "B'", 'R', 'B', "L'", "D'", 'B', 'N', "B'", "U'", "D'", 'L', "D'", 'U', 'B', "F'", "U'", "R'", "D'", "R'", 'D', "D'", 'B', 'F', 'B', "D'", "R'", "L'", "F'", 'L', "F'", 'L', "L'", "B'", "D'", 'F', "L'", "U'", "R'", "R'", 'N', "R'", "U'", 'D', 'L', "U'", 'U', "L'", "F'", 'L', 'D', 'U', 'D', 'B', 'U', "B'", 'F', 'D', "U'", "L'", "L'", "B'", 'U', "B'", "D'", "L'", "L'", "D'", 'U', "B'", 'D', "F'", "R'", 'F', "L'", 'B', "R'", 'N', 'F', "D'", 'F', "D'", 'B', 'U', "F'", 'D', 'D', 'L', "B'", 'F', 'D', "B'", 'L', 'N', 'N', "B'", 'F', "F'", 'R', 'D', 'N', 'U', "U'", "U'", 'R', "R'", 'L', "F'", "D'", 'B', 'D', 'N', 'D', "U'", "L'", "L'", "U'", "R'", 'F', "B'", "D'", 'L', "L'", 'F', 'F', 'N', "R'", 'D', "B'", 'B', "B'", 'N', 'B', "F'", 'B', 'D', 'R', "L'", "D'", "U'", "R'", 'R', 'L', "R'", 'L', "R'", "B'", 'N', 'N', 'U', "L'", "R'", "B'", 'U', 'B', 'U', 'R', "U'", "U'", "B'", "R'", 'U', "D'", "U'", 'F', "L'", 'B', 'D', 'R', 'F', "F'", "U'", "D'", 'B', 'N', 'D', 'R', 'L', "F'", "U'", 'B', "F'", "R'", 'D', "R'", "U'", "F'", "B'", "U'", "D'", "L'", 'F', 'N', 'R', 'D', 'D', 'F', "B'", 'B', "D'", 'L', 'N', 'B', "R'", 'F', "L'", "U'", 'U', 'B', 'L', "U'", "L'", 'B', "F'", "D'", "U'", "U'", 'U', "F'", 'L', "F'", "B'", "L'", "B'", "D'", "D'", 'F', "U'", "L'", "F'", 'U', 'F', 'U', "R'", "F'", "F'", "D'", 'L', "B'", "D'", 'F', 'L', 'U', "R'", 'N', 'U', 'B', "F'", "B'", "D'", 'U', "F'", "F'", 'B', 'B', "R'", 'F', "U'", 'R', 'B', "L'", "L'", "U'", "U'", "L'", "L'", "B'", 'R', "L'", 'N', 'U', 'L', 'U', 'F', "L'", 'U', 'D', "B'", "U'", 'N', 'N', "F'", "D'", 'F', 'R', 'L', "U'", 'B', "R'", "R'", 'L', 'R', "R'", "B'", 'U', 'L', "U'", "L'", "D'", "U'", "D'", 'R', "U'", "B'", "L'", "L'", "F'", 'B', "R'", 'B', "R'", 'F', "R'", 'U', 'D', "U'", "U'", 'D', 'B', "U'", 'F', 'B', "D'", "B'", "U'", "F'", 'R', "F'", 'D', "U'", 'U', 'N', "U'", 'F', "U'", 'D', "U'", 'D', "L'", "R'", "R'", 'R', 'U', 'U', "D'", "U'", 'F', "R'", 'N', 'D', "B'", 'B', "F'", "D'", "F'", 'N', 'B', "F'", "L'", "R'", "F'", 'F', 'L', 'F', 'F', 'N', "D'", 'D', 'B', "D'", "U'", "L'", "F'", 'B', "F'", "L'", "U'", "D'", "L'", 'R', 'L', "B'", "F'", "F'", 'L', "R'", 'L', 'D', "U'", 'N', "L'", "D'", "B'", 'U', "R'", "D'", "B'", 'R', 'N', "B'", 'L', 'L', "R'", 'D', 'N', 'L', "D'", "D'", "D'", 'F', "F'", "B'", "B'", "L'", 'N', "U'", "B'", 'N', "U'", 'L', "R'", "L'", "F'", 'B', 'U', 'L', 'L', 'D', "B'", "U'", "L'", 'L', 'R', "U'", "D'", "R'", "D'", 'R', 'B', 'U', 'F', "R'", 'U', 'D', 'B', 'R', 'F', 'D', "L'", 'U', "R'", 'B', "D'", "L'", "B'", "B'", "F'", "F'", "B'", "B'", "L'", 'N', "D'", "L'", 'B', 'F', "L'", 'D', "U'", 'U', 'U', 'D', "R'", "R'", "F'", "F'", 'D', 'U', 'U', 'F', "U'", "R'", 'D', 'D', 'F', 'U', "B'", "B'", 'D', 'U', 'N', "R'", "D'", "B'", 'N', 'L', "B'", "B'", 'D', 'N', "B'", "U'", 'B', 'L', "U'", 'R', 'R', "F'", 'F', 'N', 'B', "F'", "R'"]
    res = simplify_list_of_perms(test)
    print(res)

    print(Cube(2).permute(test))
    print(Cube(2).permute(res))
