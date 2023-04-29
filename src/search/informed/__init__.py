from .a_star import AStarSearchEngine
from .iterative_a_star import IterativeDeepeningAStarSearchEngine
from .step_by_step_a_star import AStarStepByStep

INFORMED_SEARCH_ENGINES = [
    AStarSearchEngine,
    IterativeDeepeningAStarSearchEngine,
    AStarStepByStep,
]
