from src.modelisation.modelisation import Cube
from src.search.evaluation.entropy import entropy_based_score_evaluation_function
from src.search.models.game_state import GameState
from src.search.uninformed.iterative_depth import IterativeDeepeningSearchEngine

if __name__ == "__main__":
    cube = Cube(3)

    engine = IterativeDeepeningSearchEngine(
        GameState(cube), entropy_based_score_evaluation_function, 3
    )
    solution = engine.run()

    print(solution.cube)
