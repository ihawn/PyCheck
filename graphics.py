import pygame
import gameagents

class Square(pygame.sprite.Sprite):
    def __init__(self, color, size):
        super(Square, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

def draw_screen(screen, linearsize):
    draw_board(screen, linearsize)
    pygame.display.flip()

def draw_board(screen, linearsize):
    squarewidth = linearsize/8
    blacksquare = Square((0, 0, 0), squarewidth)
    whitesquare = Square((255, 255, 255), squarewidth)

    for y in range(0, 8):
        for x in range(0, 8):
            if gameagents.valid_square(x, y):
                screen.blit(blacksquare.surf, (x*squarewidth, y*squarewidth))
            else:
                screen.blit(whitesquare.surf, (x*squarewidth, y*squarewidth))
    return screen