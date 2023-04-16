from src.modelisation.data import CORNERS_PER_FACE
from src.modelisation.modelisation import Cube
from src.modelisation.utils import compute_distance_to_position, verify_corner
from src.search.evaluation.CFOP.cross import white_cross_evaluation


def first_two_layer_evaluation(cube: Cube):
    score = white_cross_evaluation(cube)

    for corner in range(CORNERS_PER_FACE):  # the 4 corners of the white face should be in place
        if not verify_corner(corner, cube):
            score += compute_distance_to_position(corner, cube)

    return score
