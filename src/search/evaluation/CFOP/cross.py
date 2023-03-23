from src.modelisation.data import EDGES_PER_FACE
from src.modelisation.modelisation import Cube
from src.modelisation.utils import verify_corner, verify_edge, compute_distance_to_position


def white_cross_evaluation(cube: Cube):
    score = 0

    for edge in range(EDGES_PER_FACE):  # we consider only the white cross pieces (4 first edges)
        if not verify_edge(edge, cube):  # if edge is well-placed, no negative impact
            score += compute_distance_to_position(edge, cube)

    return score

