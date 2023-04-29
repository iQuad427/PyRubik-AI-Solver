from .depth import DepthFirstSearchEngine
from .breadth import BreadthFirstSearchEngine
from .iterative_depth import IterativeDeepeningSearchEngine

UNINFORMED_SEARCH_ENGINES = [
    DepthFirstSearchEngine,
    BreadthFirstSearchEngine,
    IterativeDeepeningSearchEngine,
]