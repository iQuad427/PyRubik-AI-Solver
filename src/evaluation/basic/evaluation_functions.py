from .distance import distance_to_good_face_evaluation_function
from .entropy import (
    entropy_based_score_evaluation_function,
    translated_entropy_based_score_evaluation_function,
)
from .membership import face_color_membership_evaluation_function

BASIC_EVALUATION_FUNCTIONS = {
    "Distance to good face": distance_to_good_face_evaluation_function,
    "Entropy": entropy_based_score_evaluation_function,
    "Translated entropy": translated_entropy_based_score_evaluation_function,
    "Face color membership": face_color_membership_evaluation_function,
}
