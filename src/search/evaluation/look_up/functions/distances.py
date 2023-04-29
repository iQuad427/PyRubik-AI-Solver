from src.modelisation.data import corners_2x2, edges, corners_3x3, resolved_cube_2x2, resolved_cube_3x3
from src.modelisation.modelisation import Cube
from src.search.evaluation.distance import distance_to_good_face_evaluation_function
from src.search.evaluation.entropy import translated_entropy_based_score_evaluation_function, \
    entropy_based_score_evaluation_function
from src.search.evaluation.look_up.data import distance_corners, distance_edges
from src.search.evaluation.membership import face_color_membership_evaluation_function
from src.search.models.game_state import GameState


def simple_distances_corners(cube: Cube, corners: dict):
    score = 0
    for corner in range(8):
        actual_colors = [cube.cube[facet] for facet in corners[corner]]
        score += len(distance_corners[(corner, tuple(actual_colors))])

    return score


def simple_distances_edges(cube: Cube):
    score = 0
    for edge in range(12):
        actual_colors = [cube.cube[facet] for facet in edges[edge]]
        score += len(distance_edges[(edge, tuple(actual_colors))])

    return score


def verify_corner(corner: int, cube: Cube):
    return [resolved_cube_3x3[facet] for facet in corners_3x3[corner]] == [cube.cube[facet] for facet in
                                                                           corners_3x3[corner]]


def verify_corner_2x2(corner: int, cube: Cube):
    return [resolved_cube_2x2[facet] for facet in corners_2x2[corner]] == [cube.cube[facet] for facet in
                                                                           corners_2x2[corner]]


def verify_edge(edge: int, cube: Cube):
    return [resolved_cube_3x3[facet] for facet in edges[edge]] == [cube.cube[facet] for facet in edges[edge]]


def white_corners_completion(state: GameState):
    score = 0
    for i in range(4):
        if not verify_corner(i, state.cube):
            score += 1

    return score


def all_corners_completion(state: GameState):
    score = 0
    for i in range(8):
        if not verify_corner(i, state.cube):
            score += 1

    return score


def all_corners_completion_2x2(state: GameState):
    score = 0
    for i in range(8):
        if not verify_corner_2x2(i, state.cube):
            score += 1

    return score


def all_edges_completion(state: GameState):
    score = 0
    for i in range(12):
        if not verify_edge(i, state.cube):
            score += 1

    return score


def white_cross_completion(state: GameState):
    score = 0
    for i in range(4):
        if not verify_edge(i, state.cube):
            score += 1

    return score


def white_face_completion(state: GameState):
    score = 0
    for i in range(4):
        if not verify_corner(i, state.cube):
            score += 1

    for i in range(4):
        if not verify_edge(i, state.cube):
            score += 1

    return score


def simple_distances_total_independent_moves_white_cross_3x3(state: GameState):
    """
    Nice for 3x3 white cross for GA : 300, 50, 8, 1, cube, simple_distances_total_independent_moves_white_cross_3x3
    """
    return (simple_distances_edges(state.cube)) * white_cross_completion(state)


def simple_distances_total_independent_moves_white_face_3x3(state: GameState):
    f = white_corners_completion(state) * simple_distances_corners(state.cube, corners_3x3)
    g = white_cross_completion(state) * simple_distances_edges(state.cube)

    return f + g


def simple_distances_total_independent_moves_all_3x3(state: GameState):
    f = all_corners_completion(state) * simple_distances_corners(state.cube, corners_3x3)
    g = all_edges_completion(state) * simple_distances_edges(state.cube)
    h = entropy_based_score_evaluation_function(state)
    i = face_color_membership_evaluation_function(state)
    j = distance_to_good_face_evaluation_function(state)

    # print("heuristic:", f, f2, g, g2, h, i, j)

    return (f + g) * h * i * j


def simple_distances_total_independent_moves_all_2x2(state: GameState):
    f = all_corners_completion_2x2(state) * simple_distances_corners(state.cube, corners_2x2)
    g = entropy_based_score_evaluation_function(state)
    h = distance_to_good_face_evaluation_function(state)

    return f * g * h


def simple_distances_total_independent_moves_3x3(state: GameState):
    return (simple_distances_edges(state.cube) + simple_distances_corners(state.cube,
                                                                          corners_3x3)) * white_cross_completion(state)


def simple_distances_total_independent_moves_2x2(state: GameState):
    h = simple_distances_corners(state.cube, corners_2x2) * white_corners_completion(state)
    g = distance_to_good_face_evaluation_function(state)
    return h + g
