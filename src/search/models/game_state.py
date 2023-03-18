from src.modelisation.modelisation import Cube, final_position


class GameState:
    def __init__(self, cube: Cube, depth: int = 0):
        self.cube = cube
        self.depth = depth

    def __bool__(self):
        return final_position(self.cube.cube)

    def get_legal_actions(self):
        return self.cube.perms

    def generate_successor(self, actions):
        return GameState(self.cube.permute(actions), self.depth + 1)
