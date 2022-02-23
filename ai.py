import random
import time
import gamemanager as gm

def select_piece_dumb_ai(pieces, side, is_double):
    possible_pieces = []
    for y in range(0, 8):
        for x in range(0, 8):
            m = []
            cap_p = []
            piece = pieces[y][x]
            mvs = gm.get_moves(piece, pieces, m, cap_p, is_double)
            if pieces[y][x].side == side and len(mvs) > 0:
                possible_pieces.append(pieces[y][x])
    choice = possible_pieces[random.randint(0, len(possible_pieces)-1)]
    print(len(possible_pieces))
    print(choice.x, choice.y)
    time.sleep(0.5)
    return pieces[choice.y][choice.x]

def select_move_dumb_ai(moves):
    time.sleep(0.5)
    return moves[random.randint(0, len(moves)-1)]