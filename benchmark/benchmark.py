import multiprocessing
from datetime import datetime
import time
from typing import List

from matplotlib import pyplot as plt

from src.evaluation import EVALUATION_FUNCTIONS
from src.modelisation.modelisation import Cube
from src.search.engines import GAME_ENGINES
from src.search.models.game_state import GameState


# Wrapper evaluation function
def wrapper_evaluation_function(evaluation_function, best_score_list: List):
    def inner(*args, **kwargs):
        score = evaluation_function(*args, **kwargs)

        # Check if score is better than the best score
        if not best_score_list or score < best_score_list[0][0] * 0.9:
            best_score_list.insert(0, (score, args[0].cube, datetime.now()))

        return score

    return inner


def run_game_engine(game_engine, evaluation_function, best_score_list, cube):
    instantiated_engine = game_engine(
        GameState(cube),
        evaluation_function=wrapper_evaluation_function(
            evaluation_function, best_score_list
        ),
    )
    instantiated_engine.run()


def compute_score_evolution_for_game_engine_and_evaluation_functions(engine_eval_runs):
    time_limit = 120  # Time limit in seconds
    results = []
    processes = []
    names = []
    a = 0
    for game_engine, evaluation_function in engine_eval_runs:
        a += 1
        if a > 20:
            break
        print(
            "Using game engine",
            game_engine.__name__,
            "and evaluation function",
            evaluation_function.__name__,
        )

        cube = Cube(3)
        cube.scramble(20)

        manager = multiprocessing.Manager()
        best_score_list = manager.list()

        game_engine_process = multiprocessing.Process(
            target=run_game_engine,
            args=(game_engine, evaluation_function, best_score_list, cube),
        )

        processes.append(game_engine_process)
        results.append(best_score_list)
        names.append(f"{game_engine.__name__} - {evaluation_function.__name__}")

    for process in processes:
        process.start()
    time.sleep(time_limit)
    for process in processes:
        process.terminate()
    prepared_data = {}
    for result, name in zip(results, names):
        # Plot score evolution with time
        scores = [score[0] for score in result]
        times = [(score[2] - result[-1][2]).total_seconds() for score in result]
        prepared_data[name] = (scores, times)
    return prepared_data


def compute_and_plot_evolution(all_configs):
    prepared_data = compute_score_evolution_for_game_engine_and_evaluation_functions(
        engine_eval_runs=all_configs
    )
    plt.clf()
    plt.figure(figsize=(30, 30))
    for name, (scores, times) in prepared_data.items():
        normalized_scores = [score / scores[-1] for score in scores]
        plt.plot(times, normalized_scores, label=name)

    # increase figure size

    plt.xlabel("Time (s)")
    plt.ylabel("Score")
    plt.title(
        f"Score evolution with time for all game engines and evaluation functions"
    )
    plt.legend()
    plt.show()


def main():
    all_configs = [
        (game_engine, evaluation_function)
        for game_engine in GAME_ENGINES
        for evaluation_function in EVALUATION_FUNCTIONS.values()
    ]

    compute_and_plot_evolution(all_configs)


if __name__ == "__main__":
    main()
