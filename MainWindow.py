import pygame
import os
from main import main

Gamemode = 2
clicked = 1
color = pygame.Color('Grey')
resolution = (640, 480)
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
resolutions_list = [(640, 480), (800, 600), (1024, 768), (1280, 720), (screen_width, screen_height)]
current_res_index = 0

pygame.init()

def calculate_positions(res, button_width=400, button_height=60):
    positions = {
        'center_x': (res[0] - button_width) // 2,
        'center_y': (res[1] - button_height) // 2,
        'button_width': button_width,
        'button_height': button_height
    }
    return positions


def draw_button(screen, rect, text, font, hover=False):
    pygame.draw.rect(screen, pygame.Color('Black' if hover else 'White'), rect)
    text_surface = font.render(text, False, pygame.Color('White' if hover else 'Black'))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def Gamemodes(k):
    global Gamemode, clicked
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(resolution)
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    pos = calculate_positions(resolution)

    Y = False
    while not Y:
        screen.fill(pygame.Color('White'))
        x, y = pygame.mouse.get_pos()

        buttons = [
            pygame.Rect(pos['center_x'], pos['center_y'] - 100, pos['button_width'], pos['button_height']),
            pygame.Rect(pos['center_x'], pos['center_y'], pos['button_width'], pos['button_height']),
            pygame.Rect(pos['center_x'], pos['center_y'] + 100, pos['button_width'], pos['button_height']),
            pygame.Rect(pos['center_x'], pos['center_y'] + 200, pos['button_width'], pos['button_height'])
        ]

        for i, (text, rect) in enumerate(zip(['Original', 'Survival', 'Puzzle', 'Back'], buttons)):
            hover = rect.collidepoint(x, y)
            draw_button(screen, rect, text, my_font, hover)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = 0
                for i, rect in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        if i == 3:
                            Y = True
                        else:
                            Gamemode = i + 1
                            if k == 1:
                                if Gamemode == 1:
                                    main(False, Gamemode, resolution)
                                elif Gamemode == 2:
                                    main(True, Gamemode, resolution)
                                elif Gamemode == 3:
                                    main(False, Gamemode, resolution)
                            elif k == 2:
                                return
        pygame.display.flip()


def Settings():
    global color, clicked, resolution, current_res_index
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(resolution)
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    pos = calculate_positions(resolution)

    while True:
        screen.fill(pygame.Color('Grey'))
        x, y = pygame.mouse.get_pos()

        buttons = [
            pygame.Rect(pos['center_x'], 200, pos['button_width'], pos['button_height']),
            pygame.Rect(pos['center_x'], 300, pos['button_width'], pos['button_height'])
        ]

        pygame.draw.rect(screen, color, (pos['center_x'] + 150, 215, 40, 40))

        for i, (text, rect) in enumerate(zip([f'Resolution: {resolution[0]}x{resolution[1]}', 'Back'], buttons)):
            hover = rect.collidepoint(x, y)
            draw_button(screen, rect, text, my_font, hover)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = 0
                for i, rect in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        if i == 0:
                            current_res_index = (current_res_index + 1) % len(resolutions_list)
                            resolution = resolutions_list[current_res_index]
                            screen = pygame.display.set_mode(resolution)
                            pos = calculate_positions(resolution)

                        elif i == 1:
                            return
        pygame.display.flip()


def mainWindow():
    global color, resolution
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(resolution)
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    pos = calculate_positions(resolution)

    while True:
        screen.fill(color)
        x, y = pygame.mouse.get_pos()

        buttons = [
            pygame.Rect(pos['center_x'], 100, pos['button_width'], pos['button_height']),
            pygame.Rect(pos['center_x'], 200, pos['button_width'], pos['button_height'])
        ]

        for i, (text, rect) in enumerate(zip(['Start Game!', 'Settings'], buttons)):
            hover = rect.collidepoint(x, y)
            draw_button(screen, rect, text, my_font, hover)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        if i == 1:
                            Settings()
                            screen = pygame.display.set_mode(resolution)
                            pos = calculate_positions(resolution)
                        if i == 0:
                            Gamemodes(1)

        pygame.display.flip()


if __name__ == "__main__":
    current_res_index = resolutions_list.index(resolution) if resolution in resolutions_list else 0
    mainWindow()
