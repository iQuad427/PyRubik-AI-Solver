import math

from src.search.generic.generic import GenericGameEngine
from src.search.informed.a_star import AStarSearchEngine
from src.search.uninformed.breadth import BreadthFirstSearchEngine
from src.search.uninformed.depth import DepthFirstSearchEngine
from src.search.uninformed.iterative_depth import IterativeDeepeningSearchEngine


class AStarStepByStep(GenericGameEngine):
    def __init__(self, starting_state, evaluation_function, max_depth=math.inf):
        super().__init__(starting_state, evaluation_function, max_depth)

    def run(self):
        i = 1

        while i < self.max_depth:
            engine = IterativeDeepeningSearchEngine(
                self.state, self.evaluation_function, 5
            )
            engine.run()

            if engine.best_found is not None:
                if engine.best_found == self.state:
                    return self.state
                print("New start state", engine.best_found)
                self.state = engine.best_found

            i += 1

            if engine.best_score == 0:
                return engine.best_found
