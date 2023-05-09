from .distance import distance_to_good_face_evaluation_function
from .entropy import entropy_based_score_evaluation_function
from .membership import face_color_membership_evaluation_function
from .combined import combined_simple_heuristics_evaluation, combined_simple_heuristics_evaluation_upscaled

BASIC_EVALUATION_FUNCTIONS = {
    "Distance to good face": distance_to_good_face_evaluation_function,
    "Entropy": entropy_based_score_evaluation_function,
    "Face color membership": face_color_membership_evaluation_function,
    "Combined simple heuristics": combined_simple_heuristics_evaluation,
    "Combined simple heuristics up-scaled": combined_simple_heuristics_evaluation_upscaled,

}
