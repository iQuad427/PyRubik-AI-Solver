import multiprocessing
from collections import defaultdict
from datetime import datetime
import time
from typing import List

from matplotlib import pyplot as plt

from src.evaluation import EVALUATION_FUNCTIONS
from src.evaluation.basic.combined import combined_simple_heuristics_evaluation_upscaled
from src.modelisation.modelisation import Cube
from src.search.engines import GAME_ENGINES
from src.search.models.game_state import GameState


# Wrapper evaluation function
def wrapper_evaluation_function(
    evaluation_function, best_score_list: List, reference_evaluation_function
):
    def inner(*args, **kwargs):
        score = evaluation_function(*args, **kwargs)
        reference_score = reference_evaluation_function(*args, **kwargs)

        # Check if score is better than the best score
        if not best_score_list or reference_score < best_score_list[0][0] * 0.99:
            best_score_list.insert(0, (reference_score, args[0].cube, datetime.now()))

        return score

    return inner


def run_game_engine(
    game_engine,
    evaluation_function,
    best_score_list,
    cube,
    reference_evaluation_function,
):
    instantiated_engine = game_engine(
        GameState(cube),
        evaluation_function=wrapper_evaluation_function(
            evaluation_function, best_score_list, reference_evaluation_function
        ),
    )
    instantiated_engine.run()


def compute_score_evolution_for_game_engine_and_evaluation_functions(
    engine_eval_runs, reference_evaluation_function
):
    time_limit = 10  # Time limit in seconds
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
            args=(
                game_engine,
                evaluation_function,
                best_score_list,
                cube,
                reference_evaluation_function,
            ),
        )

        processes.append(game_engine_process)
        results.append(best_score_list)
        names.append(f"{game_engine.__name__} - {evaluation_function.__name__}")

    for process in processes:
        process.start()

    # Display progress bar (and sleep for time_limit seconds)
    for i in range(time_limit):
        print(f"Progress: {i+1}/{time_limit} seconds")
        time.sleep(1)

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
        engine_eval_runs=all_configs,
        reference_evaluation_function=combined_simple_heuristics_evaluation_upscaled,
    )

    max_time = max(max(times) for scores, times in prepared_data.values())

    plt.clf()
    plt.figure(figsize=(15, 10))
    print(max_time)
    for name, (scores, times) in prepared_data.items():
        normalized_scores = [score / scores[-1] for score in scores]
        plt.plot(
            [max_time, *times],
            [normalized_scores[0], *normalized_scores],
            label=name.replace("DijkstraGameEngine - ", ""),
        )

    # increase figure size

    plt.xlabel("Time (s)")
    plt.ylabel("Score")
    plt.title(
        f"Score evolution with time for all game engines and evaluation functions"
    )
    plt.tight_layout(rect=[0, 0, 0.6, 1])
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.show()




def plot_box_plots_of_best_scores(all_configs, number_of_eval=20):
    best_scores = defaultdict(list)

    names_to_index = {}

    def get_index(name):
        if name not in names_to_index:
            names_to_index[name] = len(names_to_index)
        return names_to_index[name]

    for i in range(number_of_eval):
        print(f"Run {i+1}/{number_of_eval}")
        prepared_data = compute_score_evolution_for_game_engine_and_evaluation_functions(
            engine_eval_runs=all_configs,
            reference_evaluation_function=combined_simple_heuristics_evaluation_upscaled,
        )

        for name, (scores, times) in prepared_data.items():
            normalized_scores = [score / scores[-1] for score in scores]
            best_scores[get_index(name.replace("DijkstraGameEngine - ", ""))].append(normalized_scores[0])

    plt.clf()
    plt.xlabel("Game engine and evaluation function")
    plt.ylabel("Best score")
    plt.boxplot(best_scores.values(), labels=best_scores.keys())
    plt.show()

    # display table of names to index
    print(names_to_index)
    for name, index in names_to_index.items():
        print(f"{index}: {name}")

def main():
    all_configs = [
        (game_engine, evaluation_function)
        for game_engine in GAME_ENGINES
        for evaluation_function in EVALUATION_FUNCTIONS.values()
    ]

    # compute_and_plot_evolution(all_configs)

    plot_box_plots_of_best_scores(all_configs, number_of_eval=50)

if __name__ == "__main__":
    main()
