import pygame
import os

clicked = 0


def BasicGamemodes(e, m):  # просто вовзаращаю базовое меню режимов игры
    pygame.draw.rect(e, pygame.Color('White'), (200, 100, 400, 60))
    text_surface = m.render('Выживание', False, (0, 0, 0))
    e.blit(text_surface, (315, 112))

    pygame.draw.rect(e, pygame.Color('Black'), (200, 200, 400, 60))
    text_surface1 = m.render('Оригинальный', False, pygame.Color('White'))
    e.blit(text_surface1, (325, 212))

    pygame.draw.rect(e, pygame.Color('White'), (200, 300, 400, 60))
    text_surface2 = m.render('Пазл', False, (0, 0, 0))
    e.blit(text_surface2, (335, 312))


def Gamemodes():
    global clicked
    pygame.init()
    pygame.font.init()
    screen1 = pygame.display.set_mode((800, 800))
    screen1.fill(pygame.Color('White'))
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('Start Game!', False, (0, 0, 0))
    text_surface1 = my_font.render('Gamemode', False, (0, 0, 0))
    text_surface2 = my_font.render('Settings', False, (0, 0, 0))
    pygame.draw.rect(screen1, pygame.Color('White'), (200, 100, 400, 60))
    screen1.blit(text_surface, (315, 112))
    pygame.draw.rect(screen1, pygame.Color('White'), (200, 200, 400, 60))
    screen1.blit(text_surface1, (325, 212))
    pygame.draw.rect(screen1, pygame.Color('White'), (200, 300, 400, 60))
    screen1.blit(text_surface2, (335, 312))
    Y = False
    while not Y:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                mainWindow()
            x, y = map(int, pygame.mouse.get_pos())
            if 100 <= y <= 160 and 200 <= x <= 600:
                pygame.draw.rect(screen1, pygame.Color('Black'), (200, 100, 400, 60))
                text_surface = my_font.render('Выживание', False, pygame.Color('White'))
                screen1.blit(text_surface, (315, 112))
            else:
                pygame.draw.rect(screen1, pygame.Color('White'), (200, 100, 400, 60))
                text_surface = my_font.render('Выживание', False, (0, 0, 0))
                screen1.blit(text_surface, (315, 112))
            if 200 <= y <= 260 and 200 <= x <= 600:
                pygame.draw.rect(screen1, pygame.Color('Black'), (200, 200, 400, 60))
                text_surface1 = my_font.render('Оригинальный', False, pygame.Color('White'))
                screen1.blit(text_surface1, (325, 212))
            else:
                pygame.draw.rect(screen1, pygame.Color('White'), (200, 200, 400, 60))
                text_surface1 = my_font.render('Оригинальный', False, (0, 0, 0))
                screen1.blit(text_surface1, (325, 212))
            if 300 <= y <= 360 and 200 <= x <= 600:
                pygame.draw.rect(screen1, pygame.Color('Black'), (200, 300, 400, 60))
                text_surface2 = my_font.render('Пазл', False, pygame.Color('White'))
                screen1.blit(text_surface2, (335, 312))
            else:
                pygame.draw.rect(screen1, pygame.Color('White'), (200, 300, 400, 60))
                text_surface2 = my_font.render('Пазл', False, (0, 0, 0))
                screen1.blit(text_surface2, (335, 312))
            if 200 <= x <= 600 and event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= y <= 160:
                    clicked = 1
                    pygame.draw.rect(screen1, pygame.Color('Black'), (200, 100, 400, 60))
                    text_surface = my_font.render('Сохранено!', False, pygame.Color('White'))
                    screen1.blit(text_surface, (315, 112))
                elif 200 <= y <= 260:
                    clicked = 2
                    pygame.draw.rect(screen1, pygame.Color('Black'), (200, 200, 400, 60))
                    text_surface1 = my_font.render('Сохранено!', False, pygame.Color('White'))
                    screen1.blit(text_surface1, (325, 212))
                elif 300 <= y <= 360:
                    clicked = 3
                    pygame.draw.rect(screen1, pygame.Color('Black'), (200, 300, 400, 60))
                    text_surface2 = my_font.render('Сохранено', False, pygame.Color('White'))
                    screen1.blit(text_surface2, (335, 312))
        pygame.display.flip()

def mainWindow():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 800))
    screen.fill(pygame.Color('Grey'))
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
                    os.system('main.py')
                elif 200 <= y <= 260:
                    Gamemodes()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.flip()


mainWindow()
