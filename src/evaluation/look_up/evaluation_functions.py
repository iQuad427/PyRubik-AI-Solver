from src.evaluation.look_up.functions.distances import (
    simple_distances_total_independent_moves_3x3,
    simple_distances_total_independent_moves_all_3x3,
    simple_distances_total_independent_moves_all_3x3_upscaled,
)

LOOK_UP_EVALUATION_FUNCTIONS = {
    "Simple Look-Up Distance 3x3": simple_distances_total_independent_moves_3x3,
    "Simple Smoothen Look-Up Distance 3x3": simple_distances_total_independent_moves_all_3x3,
    "Simple Smoothen and Up-Scaled Look-Up Distance 3x3": simple_distances_total_independent_moves_all_3x3_upscaled,
}
