import pygame
import gameagents
from pygame import gfxdraw

class Square(pygame.sprite.Sprite):
    def __init__(self, color, size):
        super(Square, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

def draw_screen(screen, linearsize, board):
    draw_board(screen, linearsize)
    draw_pieces(screen, board.piece_arr, linearsize)
    pygame.display.flip()

def draw_board(screen, linearsize):
    squarewidth = linearsize/8
    blacksquare = Square((42, 109, 222), squarewidth*0.99)
    whitesquare = Square((199, 220, 255), squarewidth*0.99)

    for x in range(0, 8):
        for y in range(0, 8):
            if gameagents.valid_square(x, y):
                screen.blit(blacksquare.surf, (x*squarewidth, y*squarewidth))
            else:
                screen.blit(whitesquare.surf, (x*squarewidth, y*squarewidth))

def draw_pieces(screen, piece_arr, linearsize):
    squarewidth = linearsize/8
    r = squarewidth * 0.35
    black = (10, 10, 10)
    white = (250, 250, 250)
    border_b = (0, 0, 0)
    border_w = (255, 255, 255)
    for y in range(0, 8):
        for x in range(0, 8):
            pos = (piece_arr[x][y].x*squarewidth + squarewidth/2, piece_arr[x][y].y*squarewidth + squarewidth/2)
            if piece_arr[x][y].side == "black":
                #pygame.draw.circle(screen, black, pos, r)
                draw_circle(screen, pos, r, black)
            elif piece_arr[x][y].side == "white":
                #pygame.draw.circle(screen, white, pos, r)
                draw_circle(screen, pos, r, white)

def draw_circle(surface, pos, r, color):
    gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), int(r), color)
    gfxdraw.filled_circle(surface, int(pos[0]), int(pos[1]), int(r), color)
