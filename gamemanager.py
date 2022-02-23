import math
import pygame
import gameagents
import graphics
import tkinter as tk
import menu
from pygame.locals import *


class GameManager:
    def __init__(self, width, height):
        self.game_running = True
        self.width = width
        self.height = height
        self.size = width, height


def game_loop():
    root = tk.Tk()
    h = root.winfo_screenheight()
    height = h * 0.9

    pygame.init()
    gm = GameManager(height, height)
    board = gameagents.Board()
    screen = pygame.display.set_mode(gm.size)
    in_game = False
    moves = []
    piece = None
    selected_piece = None
    last_piece = None
    captured_pieces = []
    moved = False
    moved_once = False
    turn_continues = False
    new_pos = None
    captured_a_piece = False
    double_jumping_pos = None
    captured_a_piece_last_selection = False
    captured_piece_id = None
    not_turn = "white" #player whose turn it isn't

    menu_choice = [-1, -1]
    menu_choice, in_game = menu.draw_menu(screen, height, (0, 0), False, menu_choice)

    while gm.game_running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if not in_game:  # in menu
                menu_choice, in_game = menu.draw_menu(screen, height, pos, False, menu_choice)

            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    gm.game_running = False
            elif event.type == QUIT:
                gm.game_running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if not in_game:
                    menu_choice, in_game = menu.draw_menu(screen, height, pos, True, menu_choice)

                if in_game:
                    pc = piece_from_click(pos, board.piece_arr, height)

                    # movement logic
                    if pc.side != not_turn:
                        if piece is not None:
                            moves, board.piece_arr, moved, piece, captured_piece_id, captured_a_piece, new_pos = move_piece(piece, board.piece_arr, moves, height, pos, captured_pieces)
                            moved_once = True
                        else:
                            piece = piece_from_click(pos, board.piece_arr, height)

                        if piece.side != "empty":
                            selected_piece = piece
                        else:
                            selected_piece = None
                            captured_a_piece_last_selection = captured_a_piece
                        piece = piece_from_click(pos, board.piece_arr, height)
                        moves = []
                        if (not moved and not turn_continues) or \
                                (not moved and double_jumping_pos is not None and turn_continues and piece.x == double_jumping_pos[0] and piece.y == double_jumping_pos[1]):
                            moves, captured_pieces = get_moves(piece, board.piece_arr, moves, captured_pieces)

                        board.piece_arr = check_for_king(board.piece_arr)

                        if len(captured_pieces) > 0 and moved and captured_piece_id is not None and captured_a_piece:
                            x = captured_pieces[captured_piece_id].x
                            y = captured_pieces[captured_piece_id].y
                            board.piece_arr[y][x].isking = False
                            board.piece_arr[y][x].side = "empty"

                        if new_pos is not None:
                            test_piece = gameagents.Piece("black" if not_turn == "white" else "white", board, new_pos[0], new_pos[1])
                            selected_is_king = board.piece_arr[new_pos[1]][new_pos[0]].isking
                            test_piece.isking = selected_is_king
                            turn_continues = (can_jmp(test_piece, board.piece_arr) and captured_a_piece_last_selection) or not moved_once

                            if turn_continues:
                                moves, captured_pieces = get_moves(test_piece, board.piece_arr, moves, captured_pieces)
                                double_jumping_pos = (test_piece.x, test_piece.y)
                            else:
                                not_turn = "black" if not_turn == "white" else "white"
                                moved_once = False
                                double_jumping_pos = None

                            if (last_piece is None and moved_once and not turn_continues) or not moved_once:
                                last_piece = selected_piece

                        graphics.draw_screen(screen, height, board, moves, piece)


def coord_from_click(pos, size):
    x = int(8 * pos[0] / size)
    y = int(8 * pos[1] / size)
    return x, y


def piece_from_click(pos, piece_arr, size):
    pos = coord_from_click(pos, size)
    piece = piece_arr[pos[1]][pos[0]]
    return piece

def can_jmp(piece, piece_arr):
    m = []
    cap_p = []
    mvs = get_moves(piece, piece_arr, m, cap_p)
    return len(mvs[1]) > 0 #if the piece can still jump, the turn hasn't expired

# I put this together pretty quickly. There's probably a more elegant way to write this function
def get_moves(piece, piece_arr, moves, captured_pieces):
    moves = []
    captured_pieces = []
    if piece.side != "empty":
        x = piece.x
        y = piece.y
        k = 1 if piece.side == "black" else -1
        otherside = "black" if piece.side == "white" else "white"

        if 0 <= y - k < 8 and 0 <= x + k < 8:
            if piece_arr[y - k][x + k].side == "empty":
                moves.append((x + k, y - k))
            elif piece_arr[y - k][x + k].side == otherside and 0 <= y - 2*k < 8 and 0 <= x + 2*k < 8 and piece_arr[y - 2*k][x + 2*k].side == "empty":
                moves.append((x + 2*k, y - 2*k))
                captured_pieces.append(piece_arr[y - k][x + k])

        if 0 <= y - k < 8 and 0 <= x - k < 8:
            if piece_arr[y - k][x - k].side == "empty":
                moves.append((x - k, y - k))
            elif piece_arr[y - k][x - k].side == otherside and 0 <= y - 2*k < 8 and 0 <= x - 2*k < 8 and piece_arr[y - 2*k][x - 2*k].side == "empty":
                moves.append((x - 2*k, y - 2*k))
                captured_pieces.append(piece_arr[y - k][x - k])


        if piece.isking:
            if 0 <= y + k < 8 and 0 <= x - k < 8:
                if piece_arr[y + k][x - k].side == "empty":
                    moves.append((x - k, y + k))
                elif piece_arr[y + k][x - k].side == otherside and 0 <= y + 2*k < 8 and 0 <= x - 2*k < 8 and piece_arr[y + 2*k][x - 2*k].side == "empty":
                    moves.append((x - 2*k, y + 2*k))
                    captured_pieces.append(piece_arr[y + k][x - k])

            if 0 <= y + k < 8 and 0 <= x + k < 8:
                if piece_arr[y + k][x + k].side == "empty":
                    moves.append((x + k, y + k))
                elif piece_arr[y + k][x + k].side == otherside and 0 <= y + 2*k < 8 and 0 <= x + 2*k < 8 and piece_arr[y + 2*k][x + 2*k].side == "empty":
                    moves.append((x + 2*k, y + 2*k))
                    captured_pieces.append(piece_arr[y + k][x + k])

    return moves, captured_pieces


def move_piece(piece, piece_arr, moves, size, clickpos, captured_pieces):
    moved = False
    old_x = piece.x
    old_y = piece.y
    pos = coord_from_click(clickpos, size)
    captured_piece_id = None
    did_capture = False
    new_pos = None

    if pos in moves:
        if len(captured_pieces) > 0: #if a piece was captured, determine which one
            min_dis = 100
            captured_piece_id = 0
            for i in range(0, len(captured_pieces)):
                dist = math.sqrt((pos[0] - captured_pieces[i].x)**2 + (pos[1] - captured_pieces[i].x)**2)
                if dist < min_dis:
                    min_dis = dist
                    captured_piece_id = i

        if abs(old_x - pos[0]) > 1 or abs(old_y - pos[1]) > 1:
            did_capture = True

        side = piece.side
        is_king = piece.isking
        piece_arr[piece.y][piece.x].side = "empty"
        piece_arr[piece.y][piece.x].isking = False
        piece_arr[pos[1]][pos[0]].side = side
        piece_arr[pos[1]][pos[0]].isking = is_king
        moves = []
        moved = True
        new_pos = pos
    return moves, piece_arr, moved, piece, captured_piece_id, did_capture, new_pos

def check_for_king(piece_arr):
    for y in range(0, 8):
        for x in range(0, 8):
            p = piece_arr[y][x]
            if (p.side == "white" and y == 7) or (p.side == "black" and y == 0):
                piece_arr[p.y][p.x].isking = True
    return piece_arr