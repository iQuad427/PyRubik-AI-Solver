from collections import defaultdict

from matplotlib import pyplot as plt

from src.evaluation.look_up import LOOK_UP_EVALUATION_FUNCTIONS
from src.evaluation.ml import ML_EVALUATION_FUNCTIONS
from src.evaluation.basic import BASIC_EVALUATION_FUNCTIONS
from src.modelisation.modelisation import Cube
from src.search.models.game_state import GameState

MAX_RANDOM_LEVEL = 30
NUMBER_OF_RANDOM_TESTS = 10


def compute_average_score_for_evaluation_functions(
    evaluation_functions: dict, max_random_level: int, number_of_random_tests: int
):
    data_per_model = defaultdict(list)
    for function_name, evaluation_function in evaluation_functions.items():
        print("Evaluating", function_name, "...")
        for i in range(max_random_level):
            data_per_model[function_name].append([])
            for _ in range(number_of_random_tests):
                cube = Cube(3)
                cube.scramble(i)
                data_per_model[function_name][i].append(
                    evaluation_function(GameState(cube))
                )

        # Average the data and normalize it
        data_per_model[function_name] = [
            sum(data) / len(data) for data in data_per_model[function_name]
        ]

        # Normalize the data
        max_score = max(data_per_model[function_name])
        data_per_model[function_name] = [
            data / max_score for data in data_per_model[function_name]
        ]

    return data_per_model


def plot_score_evolution_with_randomness(evaluation_functions: dict):
    ml_data = compute_average_score_for_evaluation_functions(
        evaluation_functions, MAX_RANDOM_LEVEL, NUMBER_OF_RANDOM_TESTS
    )
    # Plot score evolution
    plt.figure(figsize=(10, 10))
    for name, data in ml_data.items():
        plt.plot(data, label=name)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    plot_score_evolution_with_randomness(ML_EVALUATION_FUNCTIONS)
    plot_score_evolution_with_randomness(BASIC_EVALUATION_FUNCTIONS)
    plot_score_evolution_with_randomness(LOOK_UP_EVALUATION_FUNCTIONS)
