from .best_improvement import BestImprovement
from .first_improvement import FirstImprovement
from .iterative import IteratedLocalSearch

STOCHASTIC_SEARCH_ENGINES = [
    FirstImprovement,
    BestImprovement,
    IteratedLocalSearch,
]
