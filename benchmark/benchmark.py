import threading
from datetime import datetime
from queue import Queue
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


time_limit = 1  # Time limit in seconds

results = {}

x = 0

for game_engine in GAME_ENGINES:
    for name, evaluation_function in EVALUATION_FUNCTIONS.items():
        print(
            "Using game engine", game_engine.__name__, "and evaluation function", name
        )

        cube = Cube(3)
        cube.scramble(10)

        best_score_list = []
        game_engine_thread = threading.Thread(
            target=run_game_engine,
            args=(game_engine, evaluation_function, best_score_list, cube),
        )

        game_engine_thread.start()
        print("Started")
        game_engine_thread.join(
            time_limit
        )  # Wait for the thread to finish, but only for the given time limit
        print("Finished")
        # Plot score evolution with time
        scores = [score[0] for score in best_score_list]
        times = [
            (score[2] - best_score_list[0][2]).total_seconds()
            for score in best_score_list
        ]
        print(len(scores), len(times))

        # Increase plot size
        plt.figure(figsize=(10, 10))
        plt.plot(times, scores)
        plt.xlabel("Time (s)")
        plt.ylabel("Score")
        plt.title(f"Score evolution with time for {game_engine.__name__} and {name}")
        plt.savefig(f"{game_engine.__name__}_{name}.png")
        plt.clf()

        results[f"{game_engine.__name__}_{name}"] = (scores, times)

    x += 1
    if x == 4:
        break

# Plot all results but normalize the scores and transform times to relative times in seconds

for name, (scores, times) in results.items():
    normalized_scores = [score / scores[0] for score in scores]
    relative_times = [(time - times[0]) for time in times]

    plt.plot(relative_times, normalized_scores, label=name)

plt.xlabel("Time (s)")
plt.ylabel("Score")
plt.title(f"Score evolution with time for all game engines and evaluation functions")
plt.legend()
