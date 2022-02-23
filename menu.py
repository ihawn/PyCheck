import pygame

def draw_menu(screen, screen_size, mouse_pos, clicked, choice):
    largefont = pygame.font.SysFont('Corbel', 100)
    medfont = pygame.font.SysFont('Corbel', 65)
    smallmedfont = pygame.font.SysFont('Corbel', 50)
    smallfont = pygame.font.SysFont('Corbel', 35)
    fontcolor = (255, 255, 255)
    defcolor = (100, 100, 100)
    hovercolor = (120, 120, 120)
    selectcolor = (42, 109, 222)

    start_game = False

    title = largefont.render("PyCheck", True, fontcolor)
    title_rect = title.get_rect(center=(screen_size/2, screen_size/8))
    subtitle = medfont.render("Checkers in Python", True, fontcolor)
    subtitle_rect = subtitle.get_rect(center=(screen_size/2, screen_size/8 + screen_size/12))

    p1 = smallmedfont.render("Player 1", True, fontcolor)
    p1_rect = title.get_rect(center=(2*screen_size/5 - screen_size/50, screen_size/3))
    p2 = smallmedfont.render("Player 2", True, fontcolor)
    p2_rect = title.get_rect(center=(screen_size - 2*screen_size/5 + screen_size/6, screen_size/3))

    t1 = smallfont.render("Person", True, fontcolor)
    t2 = smallfont.render("Dumb AI", True, fontcolor)
    t3 = smallfont.render("Medium AI", True, fontcolor)
    t4 = smallfont.render("Genius AI", True, fontcolor)

    start_text = largefont.render("Start Game!", True, fontcolor)

    w1 = screen_size/5
    w2 = 3*screen_size/5

    h1 = 2*screen_size/5
    h2 = 9*screen_size/20 + screen_size/40
    h3 = screen_size/2 + screen_size/20
    h4 = 11*screen_size/20 + 3*screen_size/40

    b_sizex = screen_size/5
    b_sizey = screen_size/25

    #titles
    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)
    screen.blit(p1, p1_rect)
    screen.blit(p2, p2_rect)

    #left column
    choice, start_game = DrawButton(screen, defcolor, hovercolor, selectcolor, t1, (w1, h1), b_sizex, b_sizey, mouse_pos, clicked, choice, 0, 0, False)
    choice, start_game = DrawButton(screen, defcolor, hovercolor, selectcolor, t2, (w1, h2), b_sizex, b_sizey, mouse_pos, clicked, choice, 0, 1, False)
    choice, start_game = DrawButton(screen, defcolor, hovercolor, selectcolor, t3, (w1, h3), b_sizex, b_sizey, mouse_pos, clicked, choice, 0, 2, False)
    choice, start_game = DrawButton(screen, defcolor, hovercolor, selectcolor, t4, (w1, h4), b_sizex, b_sizey, mouse_pos, clicked, choice, 0, 3, False)

    #right column
    choice, start_game = DrawButton(screen, defcolor, hovercolor, selectcolor, t1, (w2, h1), b_sizex, b_sizey, mouse_pos, clicked, choice, 1, 0, False)
    choice, start_game = DrawButton(screen, defcolor, hovercolor, selectcolor, t2, (w2, h2), b_sizex, b_sizey, mouse_pos, clicked, choice, 1, 1, False)
    choice, start_game = DrawButton(screen, defcolor, hovercolor, selectcolor, t3, (w2, h3), b_sizex, b_sizey, mouse_pos, clicked, choice, 1, 2, False)
    choice, start_game = DrawButton(screen, defcolor, hovercolor, selectcolor, t4, (w2, h4), b_sizex, b_sizey, mouse_pos, clicked, choice, 1, 3, False)

    #start game button
    if choice[0] != -1 and choice[1] != -1:
        choice, start_game = DrawButton(screen, defcolor, selectcolor, selectcolor, start_text, (screen_size/4, 2*screen_size/3 + screen_size/10), screen_size/2, screen_size/10, mouse_pos, clicked, choice, 1, 4, True)

    pygame.display.flip()
    return choice, start_game

def DrawButton(screen, col1, col2, col3, text, pos, xsize, ysize, mousepos, clicked, choice, column_id, choice_id, start):
    if pos[0] <= mousepos[0] <= pos[0] + xsize and pos[1] <= mousepos[1] <= pos[1] + ysize or choice[column_id] == choice_id:
        if clicked or (choice[column_id] == choice_id and choice_id != 4):
            pygame.draw.rect(screen, col3, [pos[0], pos[1], xsize, ysize])
            choice[column_id] = choice_id
            t_rect = text.get_rect(center=(pos[0] + xsize / 2, pos[1] + ysize / 2))
            screen.blit(text, t_rect)

            return choice, True if (clicked and choice_id == 4) else False
        else:
            pygame.draw.rect(screen, col1, [pos[0], pos[1], xsize, ysize])
    else:
        pygame.draw.rect(screen, col2, [pos[0], pos[1], xsize, ysize])

    t_rect = text.get_rect(center=(pos[0] + xsize/2, pos[1] + ysize/2))
    screen.blit(text, t_rect)
    return choice, False