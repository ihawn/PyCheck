import pygame
import gameagents
import graphics
from pygame.locals import *

class GameManager:
    def __init__(self, width, height):
        self.game_running = True
        self.width = width
        self.height = height
        self.size = width, height

def game_loop():
    pygame.init()
    gm = GameManager(1024, 1024)
    board = gameagents.Board()
    screen = pygame.display.set_mode(gm.size)

    surf = pygame.Surface((25, 25))
    surf.fill((0, 200, 255))
    rect = surf.get_rect()
    while gm.game_running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    gm.game_running = False
            elif event.type == QUIT:
                gm.game_running = False

        graphics.draw_screen(screen, 1024)