from src.search.models.game_state import GameState
from src.modelisation.data import NB_FACES_CUBE
from src.modelisation.modelisation import get_position_index


def face_color_membership_evaluation_function(state: GameState):
    """
    Compute score as number of facets having wrong color w.r.t center of the face
    :param state: the state to evaluate
    :return: score of the state
    """
    if state.cube.n % 2 != 1:
        raise NotImplementedError("Does not work for cubes with pair number of edges")

    total_score = 0

    for i in range(NB_FACES_CUBE):
        center_color = state.cube.cube[get_position_index(i, state.cube.n//2, state.cube.n//2)]
        colors = state.cube.get_face_colors(i)

        score = 0
        for color in colors:
            if color != center_color:
                score += 1

        total_score += score

    return total_score
