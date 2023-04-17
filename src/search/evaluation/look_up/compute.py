import copy

import numpy as np

from queue import Queue
from src.modelisation.data import corners_2x2, edges, resolved_cube_3x3, resolved_cube_2x2
from src.modelisation.modelisation import Cube


def create_empty_cube(size: int):
    model = []
    for _ in range(6):
        for i in range(size * size):
            model.append("N")

    return Cube(size, inner=np.array(model))


def set_corner(model: Cube, facets: list[int], colors: list[str], parity=0):
    if parity:
        model.cube[facets[0]] = colors[0]
        model.cube[facets[1]] = colors[2]
        model.cube[facets[2]] = colors[1]
        return

    for i, facet in enumerate(facets):
        model.cube[facet] = colors[i]


def set_edge(model: Cube, facets: list[int], colors: list[str]):
    for i, facet in enumerate(facets):
        model.cube[facet] = colors[i]


def verify_corner(corner: int, cube: Cube):
    return [resolved_cube_2x2[facet] for facet in corners_2x2[corner]] == [cube.cube[facet] for facet in corners_2x2[corner]]


def verify_edge(edge: int, cube: Cube):
    return [resolved_cube_3x3[facet] for facet in edges[edge]] == [cube.cube[facet] for facet in edges[edge]]


def orient(piece: list[int], turns: int):
    new_orientation = copy.deepcopy(piece)
    for _ in range(turns):
        new_orientation.append(new_orientation[0])
        new_orientation.pop(0)

    return new_orientation


def depth_search(model: Cube, piece: int, max_depth: int, type: str):
    queue = Queue()
    queue.put((0, model, []))

    while queue.qsize() != 0:
        current = queue.get()

        if type == "corner":
            if verify_corner(piece, current[1]):
                print(current)
                return current
        elif type == "edge":
            if verify_edge(piece, current[1]):
                print(current)
                return current

        if current[0] < max_depth:
            for move in model.perms:
                queue.put((current[0] + 1, current[1].permute([move]), current[2] + [move]))


def look_up_table_corners():
    distances = {}
    resolved_cube = Cube(2).cube
    for position in range(8):  # for each relative position
        print(f"<= position : {position} ================>")
        for piece in range(8):  # we try all possible corner piece
            print("piece being processed :", piece)
            for orientation in range(3):  # in all three possible orientations
                for x in range(2):
                    cube = create_empty_cube(2)
                    facets = orient(corners_2x2[piece], orientation)

                    cuby = [resolved_cube[facet] for facet in facets]
                    set_corner(cube, corners_2x2[position], cuby, parity=x)

                    result = depth_search(cube, piece, 4, "corner")
                    if result is not None:
                        distances[(position, tuple(cuby))] = result[2]

    return distances


def look_up_table_edges():
    distances = {}
    resolved_cube = Cube(3).cube
    for position in range(12):  # for each relative position
        print(f"<= position : {position} ================>")
        for piece in range(12):  # we try all possible corner piece
            print("piece being processed :", piece)
            for orientation in range(2):  # in all three possible orientations
                cube = create_empty_cube(3)
                facets = orient(edges[piece], orientation)

                cuby = [resolved_cube[facet] for facet in facets]
                set_edge(cube, edges[position], cuby)

                result = depth_search(cube, piece, 4, "edge")
                if result is not None:
                    distances[(position, tuple(cuby))] = result[2]

    return distances


if __name__ == '__main__':
    # print(look_up_table_corners())
    print(look_up_table_edges())
