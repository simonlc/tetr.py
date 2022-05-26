flags = {
    'hardDrop': 1,
    'moveRight': 2,
    'moveLeft': 4,
    'moveDown': 8,
    'holdPiece': 16,
    'rotRight': 32,
    'rotLeft': 64,
    'rot180': 128,
}

finesse = [
    [
        [1, 2, 1, 0, 1, 2, 1],
        [2, 2, 2, 2, 1, 1, 2, 2, 2, 2],
        [1, 2, 1, 0, 1, 2, 1],
        [2, 2, 2, 2, 1, 1, 2, 2, 2, 2],
    ],
    [
        [1, 2, 1, 0, 1, 2, 2, 1],
        [2, 2, 3, 2, 1, 2, 3, 3, 2],
        [2, 3, 2, 1, 2, 3, 3, 2],
        [2, 3, 2, 1, 2, 3, 3, 2, 2],
    ],
    [
        [1, 2, 1, 0, 1, 2, 2, 1],
        [2, 2, 3, 2, 1, 2, 3, 3, 2],
        [2, 3, 2, 1, 2, 3, 3, 2],
        [2, 3, 2, 1, 2, 3, 3, 2, 2],
    ],
    [
        [1, 2, 2, 1, 0, 1, 2, 2, 1],
        [1, 2, 2, 1, 0, 1, 2, 2, 1],
        [1, 2, 2, 1, 0, 1, 2, 2, 1],
        [1, 2, 2, 1, 0, 1, 2, 2, 1],
    ],
    [
        [1, 2, 1, 0, 1, 2, 2, 1],
        [2, 2, 2, 1, 1, 2, 3, 2, 2],
        [1, 2, 1, 0, 1, 2, 2, 1],
        [2, 2, 2, 1, 1, 2, 3, 2, 2],
    ],
    [
        [1, 2, 1, 0, 1, 2, 2, 1],
        [2, 2, 3, 2, 1, 2, 3, 3, 2],
        [2, 3, 2, 1, 2, 3, 3, 2],
        [2, 3, 2, 1, 2, 3, 3, 2, 2],
    ],
    [
        [1, 2, 1, 0, 1, 2, 2, 1],
        [2, 2, 2, 1, 1, 2, 3, 2, 2],
        [1, 2, 1, 0, 1, 2, 2, 1],
        [2, 2, 2, 1, 1, 2, 3, 2, 2],
    ],
]

"""
Piece data
"""
kickData = [
    [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
    [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
]
kickDataI = [
    [[0, 0], [-1, 0], [2, 0], [-1, 0], [2, 0]],
    [[-1, 0], [0, 0], [0, 0], [0, -1], [0, 2]],
    [[-1, -1], [1, -1], [-2, -1], [1, 0], [-2, 0]],
    [[0, -1], [0, -1], [0, -1], [0, 1], [0, -2]],
]
kickDataO = [[[0, 0]], [[0, 0]], [[0, 0]], [[0, 0]]]

PieceI = {
    'index': 0,
    'x': 2,
    'y': -1,
    'kickData': kickDataI,
    'tetro': [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
}
PieceJ = {
    'index': 1,
    'x': 3,
    'y': 0,
    'kickData': kickData,
    'tetro': [[2, 2, 0], [0, 2, 0], [0, 2, 0]],
}
PieceL = {
    'index': 2,
    'x': 3,
    'y': 0,
    'kickData': kickData,
    'tetro': [[0, 3, 0], [0, 3, 0], [3, 3, 0]],
}
PieceO = {
    'index': 3,
    'x': 4,
    'y': 0,
    'kickData': kickDataO,
    'tetro': [[4, 4], [4, 4]],
}
PieceS = {
    'index': 4,
    'x': 3,
    'y': 0,
    'kickData': kickData,
    'tetro': [[0, 5, 0], [5, 5, 0], [5, 0, 0]],
}
PieceT = {
    'index': 5,
    'x': 3,
    'y': 0,
    'kickData': kickData,
    'tetro': [[0, 6, 0], [6, 6, 0], [0, 6, 0]],
}
PieceZ = {
    'index': 6,
    'x': 3,
    'y': 0,
    'kickData': kickData,
    'tetro': [[7, 0, 0], [7, 7, 0], [0, 7, 0]],
}
pieces = [PieceI, PieceJ, PieceL, PieceO, PieceS, PieceT, PieceZ]

# gravityArr = range(50);
# gravityUnit = 0.00390625
# gravity = gravityUnit
# gravityArr = (function() {
#   array = []
#   array.push(0)
#   for (i = 1; i < 64; i++) array.push(i / 64)
#   for (i = 1; i <= 20; i++) array.push(i)
#   return array
# })()