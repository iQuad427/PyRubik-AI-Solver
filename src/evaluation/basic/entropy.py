import math

from src.modelisation.data import NB_FACES_CUBE
from src.search.models.game_state import GameState


def entropy_based_score_evaluation_function(state: GameState):
    """
    Evaluation function that returns the sum of the entropy of each face
    :param state:  the state to evaluate
    :return:  the score of the state
    """

    total_score = 0

    for i in range(NB_FACES_CUBE):
        colors = state.cube.get_face_colors(i)

        # Entropy as n*log(n,2) of number of colors on a face
        num_colors = len(set(colors))
        entropy = num_colors * math.log(num_colors, 2)

        total_score += entropy

    return total_score
