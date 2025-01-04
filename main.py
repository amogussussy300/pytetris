import pygame
import pymunk
import numpy as np
import random
import pymunk.pygame_util

pygame.init()
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
FPS = 144

space = pymunk.Space()
space.gravity = 0, 1000

structs = [
    np.array([
        (1, 1),
        (1, 1)
    ]),
    np.array([
        (1, 1, 1, 1)
    ]),
    np.array([
        (1,),
        (1,),
        (1,),
        (1,)
    ]),
    np.array([
        (0, 1),
        (1, 1),
        (1, 0)
    ]),
    np.array([
        (1, 1, 0),
        (0, 1, 1)
    ]),
    np.array([
        (0, 1, 1),
        (1, 1, 0)
    ])
]


def create_shape_from_struct(space, struct, position=(400, 50), cell_size=20, color=(255, 255, 255, 255)):
    body = pymunk.Body(16, 100)
    body.position = position
    space.add(body)

    rows, cols = struct.shape
    shapes = []

    for row in range(rows):
        for col in range(cols):
            if struct[row, col] == 1:
                x_offset = col * cell_size - (cols * cell_size) // 2
                y_offset = -row * cell_size + (rows * cell_size) // 2
                vertices = [
                    (x_offset, y_offset),
                    (x_offset + cell_size, y_offset),
                    (x_offset + cell_size, y_offset - cell_size),
                    (x_offset, y_offset - cell_size)
                ]

                shape = pymunk.Poly(body, vertices)
                shape.density = 1.5
                shape.elasticity = 0.1
                shape.friction = 0.5
                shape.color = (*color, 255)
                space.add(shape)
                shapes.append(shape)

    return shapes


def create_ground(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (0, 550), (800, 550), 5)
    shape.elasticity = 0.1
    shape.friction = 0.7
    space.add(body, shape)


create_ground(space)


def main():
    draw_options = pymunk.pygame_util.DrawOptions(display)
    draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                struct = random.choice(structs)
                color = tuple(random.randrange(20, 236) for i in range(3))
                create_shape_from_struct(space, struct, color=color)

        display.fill((200, 200, 200))
        pygame.draw.line(display, (50, 50, 50), (0, 550), (800, 550), 5)

        space.debug_draw(draw_options)

        space.step(1 / FPS)
        pygame.display.flip()
        clock.tick(FPS)


main()
pygame.quit()
