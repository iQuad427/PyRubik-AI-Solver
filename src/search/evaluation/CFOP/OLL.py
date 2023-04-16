from src.modelisation.modelisation import Cube
from src.modelisation.utils import face_is_complete
from src.search.evaluation.CFOP.F2L import first_two_layer_evaluation


def orientation_last_layer_evaluation(cube: Cube):
    score = first_two_layer_evaluation(cube)

    if not face_is_complete(0, cube):
        score += len(set(cube.get_face_colors(0)))  # TODO: could be a better evaluation function

    return score
