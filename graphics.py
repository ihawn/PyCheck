import pygame
import gameagents
from pygame import gfxdraw


class Square(pygame.sprite.Sprite):
    def __init__(self, color, size):
        super(Square, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()


def draw_screen(screen, linearsize, board, moves, piece, game_over, winner):
    screen.fill((0, 0, 0))
    draw_board(screen, linearsize)
    if len(moves) > 0:
        draw_potential_moves(screen, linearsize, moves, piece)
    draw_pieces(screen, board.piece_arr, linearsize)

    if game_over:
        largefont = pygame.font.SysFont('Corbel', 150)
        medfont = pygame.font.SysFont('Corbel', 100)
        col = (0, 0, 0)
        prompt = largefont.render(winner + " Wins!", True, 0)
        subtitle = medfont.render("Press Backspace", True, col)
        rect = prompt.get_rect(center=(linearsize / 2, linearsize / 4))
        subtitle_rect = subtitle.get_rect(center=(linearsize / 2, linearsize / 4 + linearsize / 4))
        screen.blit(prompt, rect)
        screen.blit(subtitle, subtitle_rect)

    pygame.display.flip()


def draw_board(screen, linearsize):
    squarewidth = linearsize / 8
    blacksquare = Square((42, 109, 222), squarewidth * 0.99)
    whitesquare = Square((199, 220, 255), squarewidth * 0.99)

    for x in range(0, 8):
        for y in range(0, 8):
            if gameagents.valid_square(x, y):
                screen.blit(blacksquare.surf, (x * squarewidth, y * squarewidth))
            else:
                screen.blit(whitesquare.surf, (x * squarewidth, y * squarewidth))


def draw_pieces(screen, piece_arr, linearsize):
    squarewidth = linearsize / 8
    r = squarewidth * 0.35
    black = (10, 10, 10)
    white = (250, 250, 250)
    crownsize = squarewidth*0.15

    crown = Square((50, 50, 180), crownsize)
    border_b = (0, 0, 0)
    border_w = (255, 255, 255)
    for y in range(0, 8):
        for x in range(0, 8):
            pos = (piece_arr[x][y].x * squarewidth + squarewidth / 2, piece_arr[x][y].y * squarewidth + squarewidth / 2)
            if piece_arr[x][y].side == "black":
                draw_circle(screen, pos, r, black)
            elif piece_arr[x][y].side == "white":
                draw_circle(screen, pos, r, white)
            if piece_arr[x][y].side != "empty" and piece_arr[x][y].isking:
                crownpos = (pos[0] - crownsize/2, pos[1] - crownsize/2)
                screen.blit(crown.surf, crownpos)


def draw_potential_moves(screen, linearsize, moves, piece):
    squarewidth = linearsize / 8
    r = squarewidth * 0.38
    highlight_color = (255, 60, 0)

    if piece is not None and piece.side != "empty":
        pos = (piece.x*squarewidth + squarewidth/2, piece.y*squarewidth + squarewidth/2)
        draw_circle(screen, pos, r, highlight_color)

    for i in range(0, len(moves)):
        x = moves[i][0]
        y = moves[i][1]
        draw_square_highlight(screen, linearsize, x, y)


def draw_circle(surface, pos, r, color):
    gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), int(r), color)
    gfxdraw.filled_circle(surface, int(pos[0]), int(pos[1]), int(r), color)


def draw_square_highlight(screen, linearsize, x, y):
    squarewidth = linearsize / 8
    highlightsquare = Square((0, 160, 255), squarewidth * 0.99)
    screen.blit(highlightsquare.surf, (x * squarewidth, y * squarewidth))
