import math

import pygame
import gameagents
import graphics
import tkinter as tk
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
    moves = []
    piece = None
    captured_pieces = []
    moved = False
    captured_a_piece = False
    captured_piece_id = None

    graphics.draw_screen(screen, height, board, moves, piece)
    while gm.game_running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    gm.game_running = False
            elif event.type == QUIT:
                gm.game_running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if piece != None:
                    moves, board.piece_arr, moved, piece, captured_piece_id, captured_a_piece = move_piece(piece, board.piece_arr, moves, height, pos, captured_pieces)
                else:
                    piece = piece_from_click(pos, board.piece_arr, height)

                piece = piece_from_click(pos, board.piece_arr, height)
                if not moved:
                    moves = []
                    captured_pieces = []
                    moves, captured_pieces = get_moves(piece, board.piece_arr, moves, captured_pieces)

                board.piece_arr = check_for_king(board.piece_arr)

                if len(captured_pieces) > 0 and moved and captured_piece_id is not None and captured_a_piece:
                    x = captured_pieces[captured_piece_id].x
                    y = captured_pieces[captured_piece_id].y
                    board.piece_arr[y][x].isking = False
                    board.piece_arr[y][x].side = "empty"

                graphics.draw_screen(screen, height, board, moves, piece)


def coord_from_click(pos, size):
    x = int(8 * pos[0] / size)
    y = int(8 * pos[1] / size)
    return x, y


def piece_from_click(pos, piece_arr, size):
    pos = coord_from_click(pos, size)
    piece = piece_arr[pos[1]][pos[0]]
    return piece

# I put this together pretty quickly. There's probably a more elegant way to write this function
def get_moves(piece, piece_arr, moves, captured_pieces):
    temp_moves = []
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
    return moves, piece_arr, moved, piece, captured_piece_id, did_capture

def check_for_king(piece_arr):
    for y in range(0, 8):
        for x in range(0, 8):
            p = piece_arr[y][x]
            if (p.side == "white" and y == 7) or (p.side == "black" and y == 0):
                piece_arr[p.y][p.x].isking = True
    return piece_arr
