import pygame
import os
from main import main

Gamemode = 2
clicked = 1
color = pygame.Color('Grey')
resolution = (800, 800)


def Gamemodes(k):
    global Gamemode
    global clicked
    pygame.init()
    pygame.font.init()
    screen1 = pygame.display.set_mode(resolution)
    screen1.fill(pygame.Color('White'))
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('Start Game!', False, (0, 0, 0))
    text_surface1 = my_font.render('Gamemode', False, (0, 0, 0))
    text_surface2 = my_font.render('Settings', False, (0, 0, 0))
    pygame.draw.rect(screen1, pygame.Color('White'), (200, 200, 400, 60))
    screen1.blit(text_surface, (315, 212))
    pygame.draw.rect(screen1, pygame.Color('White'), (200, 300, 400, 60))
    screen1.blit(text_surface1, (325, 312))
    pygame.draw.rect(screen1, pygame.Color('White'), (200, 400, 400, 60))
    screen1.blit(text_surface2, (335, 412))
    Y = False
    while not Y:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                mainWindow()
            x, y = map(int, pygame.mouse.get_pos())
            if 200 <= y <= 260 and 200 <= x <= 600:
                pygame.draw.rect(screen1, pygame.Color('Black'), (200, 200, 400, 60))
                text_surface = my_font.render('Оригинальный', False, pygame.Color('White'))
                screen1.blit(text_surface, (315, 212))
            else:
                pygame.draw.rect(screen1, pygame.Color('White'), (200, 200, 400, 60))
                text_surface = my_font.render('Оригинальный', False, (0, 0, 0))
                screen1.blit(text_surface, (315, 212))
            if 300 <= y <= 360 and 200 <= x <= 600:
                pygame.draw.rect(screen1, pygame.Color('Black'), (200, 300, 400, 60))
                text_surface1 = my_font.render('Выживание', False, pygame.Color('White'))
                screen1.blit(text_surface1, (325, 312))
            else:
                pygame.draw.rect(screen1, pygame.Color('White'), (200, 300, 400, 60))
                text_surface1 = my_font.render('Выживание', False, (0, 0, 0))
                screen1.blit(text_surface1, (325, 312))
            if 400 <= y <= 460 and 200 <= x <= 600:
                pygame.draw.rect(screen1, pygame.Color('Black'), (200, 400, 400, 60))
                text_surface2 = my_font.render('Пазл', False, pygame.Color('White'))
                screen1.blit(text_surface2, (335, 412))
            else:
                pygame.draw.rect(screen1, pygame.Color('White'), (200, 400, 400, 60))
                text_surface2 = my_font.render('Пазл', False, (0, 0, 0))
                screen1.blit(text_surface2, (335, 412))
            if 200 <= x <= 600 and event.type == pygame.MOUSEBUTTONUP and clicked == 0:
                if 200 <= y <= 260:
                    Gamemode = 1
                    if k == 2:
                        pygame.quit()
                        mainWindow()
                    return
                elif 300 <= y <= 360:
                    Gamemode = 2
                    if k == 2:
                        pygame.quit()
                        mainWindow()
                    return
                elif 400 <= y <= 460:
                    Gamemode = 3
                    if k == 2:
                        pygame.quit()
                        mainWindow()
                    return
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = 0
        pygame.display.flip()
def Settings():
    global color
    global clicked
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    Col_Surf = my_font.render('Color', False, pygame.Color('Black'))
    screen2 = pygame.display.set_mode((800, 800))
    screen2.fill(pygame.Color('Grey'))
    pygame.draw.rect(screen2, pygame.Color('White'), (100, 100, 400, 60))
    screen2.blit(Col_Surf, (120, 112))
    pygame.draw.rect(screen2, color, (370, 110, 40, 40), 25)
    while True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                mainWindow()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = 0
            if 370 <= x <= 410 and 110 <= y <= 150 and event.type == pygame.MOUSEBUTTONDOWN and clicked == 0:
                pass
        pygame.display.flip()

def mainWindow():
    global color
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 800))
    screen.fill(pygame.Color(color))
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('Start Game!', False, (0, 0, 0))
    text_surface1 = my_font.render('Gamemode', False, (0, 0, 0))
    text_surface2 = my_font.render('Settings', False, (0, 0, 0))
    pygame.draw.rect(screen, pygame.Color('White'), (200, 100, 400, 60))
    screen.blit(text_surface, (315, 112))
    pygame.draw.rect(screen, pygame.Color('White'), (200, 200, 400, 60))
    screen.blit(text_surface1, (325, 212))
    pygame.draw.rect(screen, pygame.Color('White'), (200, 300, 400, 60))
    screen.blit(text_surface2, (335, 312))
    Y = False
    while not Y:
        for event in pygame.event.get():
            x, y = map(int, pygame.mouse.get_pos())
            if 100 <= y <= 160 and 200 <= x <= 600:
                pygame.draw.rect(screen, pygame.Color('Black'), (200, 100, 400, 60))
                text_surface = my_font.render('Start Game!', False, pygame.Color('White'))
                screen.blit(text_surface, (315, 112))
            else:
                pygame.draw.rect(screen, pygame.Color('White'), (200, 100, 400, 60))
                text_surface = my_font.render('Start Game!', False, (0, 0, 0))
                screen.blit(text_surface, (315, 112))
            if 200 <= y <= 260 and 200 <= x <= 600:
                pygame.draw.rect(screen, pygame.Color('Black'), (200, 200, 400, 60))
                text_surface1 = my_font.render('Gamemode', False, pygame.Color('White'))
                screen.blit(text_surface1, (325, 212))
            else:
                pygame.draw.rect(screen, pygame.Color('White'), (200, 200, 400, 60))
                text_surface1 = my_font.render('Gamemode', False, (0, 0, 0))
                screen.blit(text_surface1, (325, 212))
            if 300 <= y <= 360 and 200 <= x <= 600:
                pygame.draw.rect(screen, pygame.Color('Black'), (200, 300, 400, 60))
                text_surface2 = my_font.render('Settings', False, pygame.Color('White'))
                screen.blit(text_surface2, (335, 312))
            else:
                pygame.draw.rect(screen, pygame.Color('White'), (200, 300, 400, 60))
                text_surface2 = my_font.render('Settings', False, (0, 0, 0))
                screen.blit(text_surface2, (335, 312))
            if 200 <= x <= 600 and event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= y <= 160:
                    Gamemodes(1)
                    print(Gamemode)
                    main(False, Gamemode, resolution)
                    exit()
                elif 200 <= y <= 260:
                    Gamemodes(2)
                    main(False, Gamemode, resolution)
                elif 300 <= y <= 360:
                    Settings()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.flip()

mainWindow()
