from src.modelisation.data import NB_FACES_CUBE, face_color, dist
from src.search.models.game_state import GameState


def distance_to_good_face_evaluation_function(state: GameState):
    """
    Compute score as the manhattan distance from facet current face to facet supposed face
    :param state: the state to evaluate
    :return: score of the state
    """
    total_score = 0

    for i in range(NB_FACES_CUBE):
        score = 0
        for color in state.cube.get_face_colors(i):
            good_position = face_color[color]
            score += dist[i, good_position]

        total_score += score

    return total_score
