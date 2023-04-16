from src.modelisation.modelisation import Cube
from src.modelisation.utils import face_is_complete, compute_distance_to_position
from src.modelisation.data import CORNERS_PER_FACE, EDGES_PER_FACE, NUMBER_OF_EDGES, NUMBER_OF_CORNERS
from src.search.evaluation.CFOP.OLL import orientation_last_layer_evaluation


def permutation_last_layer_evaluation(cube: Cube):
    score = orientation_last_layer_evaluation(cube)

    if not face_is_complete(0, cube):
        for edge in range(EDGES_PER_FACE * 2, NUMBER_OF_EDGES):
            score += compute_distance_to_position(edge, cube)

        for corner in range(CORNERS_PER_FACE, NUMBER_OF_CORNERS):
            score += compute_distance_to_position(corner, cube)

    return score
