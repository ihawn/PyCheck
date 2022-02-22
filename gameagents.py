class Player:
    def __init__(self, side, pieces):
        self.side = side
        self.myturn = side == "black"
        self.pieces = pieces
        self.piecescount = len(pieces)

class Board:
    def __init__(self):
        piece_arr = []
        for y in range(0, 8):
            row = []
            for x in range(0, 8):
                if valid_square(x, y):
                    if y >= 5:
                        row.append(Piece("black", self, x, y))
                    elif y <= 2:
                        row.append(Piece("white", self, x, y))
                    else:
                        row.append(Piece("empty", self, x, y))
                else:
                    row.append(Piece("empty", self, x, y))
            piece_arr.append(row)
        self.piece_arr = piece_arr

class Piece:
    def __init__(self, side, board, x, y):
        self.side = side
        self.board = board
        self.x = x
        self.y = y
        self.isking = False

def valid_square(x, y):
    return ((x + 1) % 2 == 0 and y % 2 == 0) or ((x + 1) % 2 == 1 and y % 2 == 1)