import math
import random

from src.search.generic.generic import GenericGameEngine
from src.search.informed.a_star import AStarSearchEngine
from src.search.models.game_state import GameState
from src.search.uninformed.breadth import BreadthFirstSearchEngine
from src.search.uninformed.depth import DepthFirstSearchEngine
from src.search.uninformed.iterative_depth import IterativeDeepeningSearchEngine


class AStarStepByStep(GenericGameEngine):
    def __init__(self, starting_state, evaluation_function, max_depth=math.inf):
        super().__init__(starting_state, evaluation_function, max_depth)

    def run(self):
        i = 1

        while i < self.max_depth:
            engine = BreadthFirstSearchEngine(self.state, self.evaluation_function, 4)
            engine.run()

            solutions = []
            solutions_score = []

            for best_found in engine.best_founds:
                new_engine = DepthFirstSearchEngine(
                    GameState(best_found.cube),
                    self.evaluation_function,
                    4,
                )

                new_engine.run()

                for best_found in new_engine.best_founds:
                    new_engine = DepthFirstSearchEngine(
                        GameState(best_found.cube),
                        self.evaluation_function,
                        3,
                    )
                    new_engine.run()

                    solutions.extend(new_engine.best_founds)
                    solutions_score.extend(new_engine.best_scores)

            best_score = min(solutions_score)

            self.state = solutions[solutions_score.index(best_score)]

            # 50% chance of random move
            if random.random() < 0.5:
                self.state.cube.scramble(random.randint(1, 10))

            i += 1
