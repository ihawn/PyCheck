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
    moved = False

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
                    moves, board.piece_arr, moved, piece = move_piece(piece, board.piece_arr, moves, height, pos)
                else:
                    piece = piece_from_click(pos, board.piece_arr, height)

                piece = piece_from_click(pos, board.piece_arr, height)
                if not moved:
                    moves = get_moves(piece, board.piece_arr, moves)

                board.piece_arr = check_for_king(board.piece_arr)
                graphics.draw_screen(screen, height, board, moves, piece)


def coord_from_click(pos, size):
    x = int(8 * pos[0] / size)
    y = int(8 * pos[1] / size)
    return x, y


def piece_from_click(pos, piece_arr, size):
    pos = coord_from_click(pos, size)
    piece = piece_arr[pos[1]][pos[0]]
    return piece


def get_moves(piece, piece_arr, moves):
    if piece.side != "empty":
        moves = []
        x = piece.x
        y = piece.y
        k = 1 if piece.side == "black" else -1

        if 0 <= y - k < 8 and 0 <= x + k < 8 and piece_arr[y - k][x + k].side == "empty":
            moves.append((x + k, y - k))
        if 0 <= y - k < 8 and 0 <= x - k < 8 and piece_arr[y - k][x - k].side == "empty":
            moves.append((x - k, y - k))
        if piece.isking:
            if 0 <= y + k < 8 and 0 <= x - k < 8 and piece_arr[y + k][x - k].side == "empty":
                moves.append((x - k, y + k))
            if 0 <= y + k < 8 and 0 <= x + k < 8 and piece_arr[y + k][x + k].side == "empty":
                moves.append((x + k, y + k))
    return moves


def move_piece(piece, piece_arr, moves, size, clickpos):
    moved = False
    old_x = piece.x
    old_y = piece.y
    pos = coord_from_click(clickpos, size)
    if pos in moves:
        side = piece.side
        is_king = piece.isking
        piece_arr[piece.y][piece.x].side = "empty"
        piece_arr[piece.y][piece.x].isking = False
        piece_arr[pos[1]][pos[0]].side = side
        piece_arr[pos[1]][pos[0]].isking = is_king
        moves = []
        moved = True
    return moves, piece_arr, moved, piece

def check_for_king(piece_arr):
    for y in range(0, 8):
        for x in range(0, 8):
            p = piece_arr[y][x]
            if (p.side == "white" and y == 7) or (p.side == "black" and y == 0):
                piece_arr[p.y][p.x].isking = True
    return piece_arr
