import numpy as np

NB_FACES_CUBE = 6
FACETS = 9
COLORS = "RBWVOJ"
COLORS_INT = [0, 1, 2, 3, 4, 5]
n = 3

resolved_cube = [
    'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y',
    'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
    'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R',
    'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
    'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
    'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'
]

moves = [
    "U",
    "L",
    "F",
    "R",
    "B",
    "D",
]  # up, right, front, left, back, down (order defined by the model)
colors = ["Y", "B", "R", "G", "O", "W"]  # yellow, blue, red, green, orange, white

face_color = {"Y": 0, "B": 1, "R": 2, "G": 3, "O": 4, "W": 5}

dist = np.array(
    [
        [0, 1, 1, 1, 1, 2],
        [1, 0, 1, 2, 1, 1],
        [1, 1, 0, 1, 2, 1],
        [1, 2, 1, 0, 1, 1],
        [1, 1, 2, 1, 0, 1],
        [2, 1, 1, 1, 1, 0],
    ]
)

NUMBER_OF_EDGES = 12
EDGES_PER_FACE = 4
edges = {
    0:  [46, 25],
    1:  [48, 16],
    2:  [50, 34],
    3:  [52, 43],
    4:  [41, 12],
    5:  [21, 14],
    6:  [23, 30],
    7:  [39, 32],
    8:  [1, 37],
    9:  [3, 10],
    10: [5, 28],
    11: [7, 19]
}

NUMBER_OF_CORNERS = 8
CORNERS_PER_FACE = 4
corners = {
    0: [45, 24, 17],
    1: [47, 26, 33],
    2: [51, 44, 15],
    3: [53, 42, 35],
    4: [6, 18, 11],
    5: [8, 20, 27],
    6: [0, 38, 9],
    7: [2, 36, 29]
}