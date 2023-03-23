import random
from typing import List

from data import *
from utils import *


class Cube:
    def __init__(self, dim, inner=None):
        self.n = dim

        if inner is not None:
            self.cube = inner
        else:
            self.cube = self._generate_cube()

        self.perms = generate_lateral_moves()
        # self.perms.update(generate_crown_moves())
        self.perms.update(generate_inverse_moves(self.perms))

    def __bool__(self):
        return final_position(self.cube)

    def __str__(self):
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

    def permute(self, perms: list[str]):
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
            save = list(new_cube)
            mvt = self.perms[perm]
            for t in mvt:
                u = (t[-1],) + t
                for i, v in enumerate(t):
                    new_cube[v] = save[u[i]]

    def get_face_colors(self, face: int) -> List[str]:
        return self.cube[face * self.n * self.n: (face + 1) * self.n * self.n]

    def get_color(self, face: int, row: int, col: int) -> List[str]:
        return self.cube[face * self.n * self.n + row * self.n + col]

    def int_list(self):
        int_data = []

        for color in self.cube:
            int_data.append(colors.index(color))

        return int_data


def get_position_index(face: int, row: int, col: int):
    return n * n * face + n * row + col


def generate_crown_moves():
    # TODO : moving centers might be bad for the algorithms -> might keep only non-center crowns permutation
    permutations = {}

    # Transversal crown permutations
    for i in range(1, n - 1):
        permutation_m = []
        permutation_e = []
        permutation_s = []
        for j in range(n):
            # M - Transversal crown permutations - starts from face 1 (then 2, 3, 4)
            permutation_m.append(
                (
                    get_position_index(0, j, i),
                    get_position_index(2, j, i),
                    get_position_index(5, j, i),
                    get_position_index(4, n - j - 1, n - i - 1),
                )
            )
        if n % 2 == 0 or i != n // 2:
            permutation_m = []
            permutation_e = []
            permutation_s = []
            for j in range(n):
                # M - Transversal crown permutations - starts from face 1 (then 2, 3, 4)
                permutation_m.append(
                    (
                        get_position_index(0, j, i),
                        get_position_index(2, j, i),
                        get_position_index(5, j, i),
                        get_position_index(4, n - j - 1, n - i - 1),
                    )
                )

                # E - Sagittal crown permutations - starts from face 0 (then 2, 5, 4)
                permutation_e.append(
                    (
                        get_position_index(1, i, j),
                        get_position_index(2, i, j),
                        get_position_index(3, i, j),
                        get_position_index(4, i, j),
                    )
                )

                # S - Frontal crown permutation - starts from face 0 (then 3', 5, 1')
                permutation_s.append(
                    (
                        get_position_index(0, i, j),
                        get_position_index(3, j, i),
                        get_position_index(5, n - i - 1, n - j - 1),
                        get_position_index(1, n - j - 1, i),
                    )
                )

            permutations[f"{i}M"] = permutation_m
            permutations[f"{i}E"] = permutation_e
            permutations[f"{i}S"] = permutation_s

    return permutations


def generate_lateral_moves():
    permutations = {}

    for face, move in enumerate(moves):
        # corners permutation : 1
        permutation = [
            (
                get_position_index(face, 0, 0),
                get_position_index(face, 0, 2),
                get_position_index(face, 2, 2),
                get_position_index(face, 2, 0),
            )
        ]

        # edges permutations : n - 2 (from 1 to n - 1)
        for i in range(1, n):
            permutation.append(
                (
                    get_position_index(face, 0, i),
                    get_position_index(face, i, n - 1),
                    get_position_index(face, n - 1, n - i - 1),
                    get_position_index(face, n - i - 1, 0),
                )
            )

        # edges permutation : n
        if move == "U":
            for j in range(n):
                permutation.append(
                    (  # 0 : Up face - 4, 3, 2, 1
                        get_position_index(4, 0, j),
                        get_position_index(3, 0, j),
                        get_position_index(2, 0, j),
                        get_position_index(1, 0, j),
                    )
                )

        if move == "L":
            for j in range(n):
                permutation.append(
                    (  # 1 : Left face - 0, 2, 5, 4
                        get_position_index(0, j, 0),
                        get_position_index(2, j, 0),
                        get_position_index(5, j, 0),
                        get_position_index(4, n - j - 1, n - 1),
                    )
                )
        if move == "F":
            for j in range(n):
                permutation.append(
                    (  # 2 : Front face - 0, 3, 5, 1
                        get_position_index(0, n - 1, j),
                        get_position_index(3, j, 0),
                        get_position_index(5, 0, n - j - 1),
                        get_position_index(1, n - j - 1, n - 1),
                    )
                )

        if move == "R":
            for j in range(n):
                permutation.append(
                    (  # 3 : Right face - 5, 2, 0, 4
                        get_position_index(5, j, n - 1),
                        get_position_index(2, j, n - 1),
                        get_position_index(0, j, n - 1),
                        get_position_index(4, n - j - 1, 0),
                    )
                )

        if move == "B":
            for j in range(n):
                permutation.append(
                    (  # 4 : Back face - 0, 1, 5, 3
                        get_position_index(0, 0, n - j - 1),
                        get_position_index(1, j, 0),
                        get_position_index(5, n - 1, j),
                        get_position_index(3, n - j - 1, n - 1),
                    )
                )

        if move == "D":
            for j in range(n):
                permutation.append(
                    (  # 5 : Down face - 1, 2, 3, 4
                        get_position_index(1, n - 1, j),
                        get_position_index(2, n - 1, j),
                        get_position_index(3, n - 1, j),
                        get_position_index(4, n - 1, j),
                    )
                )

        permutations[move] = permutation

    return permutations


if __name__ == "__main__":
    cube = Cube(3)
    # scramble = cube.scramble(5)
    #
    # print(scramble)
    # cube.permute(["U'", "L", "L", "B"])
    # print(cube)

    # cube.permute(["1S"])
    # cube.permute(["1E'"])

    # print(cube.permute("1M"))
    # print(cube.permute("1M"))
    # print(cube.permute("1E"))
    # print(cube.permute("1E"))
    # print(cube.permute("1S"))
    # print(cube.permute("1S"))

