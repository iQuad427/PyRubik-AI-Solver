from .dijkstra import DIJKSTRA_SEARCH_ENGINES
from .informed import INFORMED_SEARCH_ENGINES
from .stochastic import STOCHASTIC_SEARCH_ENGINES
from .uninformed import UNINFORMED_SEARCH_ENGINES

GAME_ENGINES = [
    *DIJKSTRA_SEARCH_ENGINES,
    # *INFORMED_SEARCH_ENGINES,
    # *STOCHASTIC_SEARCH_ENGINES,
    # *UNINFORMED_SEARCH_ENGINES,
]
