from src.modelisation.modelisation import Cube


class GameState:
    def __init__(self, cube: Cube, depth: int = 0):
        self.cube = cube
        self.depth = depth

    def get_legal_actions(self):
        return self.cube.perms

    def generate_successor(self, action):
        return GameState(self.cube.permute([action]), self.depth + 1)
