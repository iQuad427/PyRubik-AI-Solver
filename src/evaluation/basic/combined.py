from .distance import distance_to_good_face_evaluation_function
from .entropy import entropy_based_score_evaluation_function
from .membership import face_color_membership_evaluation_function
from ...search.models.game_state import GameState


def combined_simple_heuristics_evaluation_upscaled(state: GameState):
    f = distance_to_good_face_evaluation_function(state)
    g = entropy_based_score_evaluation_function(state)
    h = face_color_membership_evaluation_function(state)
    return f * g * h


def combined_simple_heuristics_evaluation(state: GameState):
    f = distance_to_good_face_evaluation_function(state)
    g = entropy_based_score_evaluation_function(state)
    h = face_color_membership_evaluation_function(state)
    return f + g + h
