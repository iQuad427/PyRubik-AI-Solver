from src.evaluation.look_up.functions.distances import (
    all_corners_completion,
    all_edges_completion,
    simple_distances_total_independent_moves_3x3,
    simple_distances_total_independent_moves_all_3x3,
    simple_distances_total_independent_moves_white_cross_3x3,
    simple_distances_total_independent_moves_white_face_3x3,
    white_corners_completion,
    white_cross_completion,
    white_face_completion,
)

LOOK_UP_EVALUATION_FUNCTIONS = {
    "White Cross Completion": white_cross_completion,
    "White Face Completion": white_face_completion,
    "White Corners Completion": white_corners_completion,
    "All Corners Completion": all_corners_completion,
    "All Edges Completion": all_edges_completion,
    "Simple Distances Total Independent Moves White Cross 3x3": simple_distances_total_independent_moves_white_cross_3x3,
    "Simple Distances Total Independent Moves White Face 3x3": simple_distances_total_independent_moves_white_face_3x3,
    "Simple Distances Total Independent Moves 3x3": simple_distances_total_independent_moves_3x3,
    "Simple Distances Total Independent Moves All 3x3": simple_distances_total_independent_moves_all_3x3,
}
