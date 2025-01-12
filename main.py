import math

import pygame
import pymunk
import numpy as np
import random
import pymunk.pygame_util
from pymunk import Body

pygame.init()
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
FPS = 144
collided_bodies = []
space = pymunk.Space()
space.gravity = 0, 850


def change_body_type(space, body, b_type):
    """
    :param space: select pymunk space
    :param body: select pymunk body
    :param b_type: select type: static, dynamic, kinematic
    """
    space.remove(body)

    if b_type == 'static':
        body.body_type = pymunk.Body.STATIC
    elif b_type == 'dynamic':
        body.body_type = pymunk.Body.DYNAMIC
    elif b_type == 'kinematic':
        body.body_type = pymunk.Body.KINEMATIC
    else:
        raise ValueError("Body type is incorrect")

    space.add(body)


def begin_collision(arbiter, space, data):
    shape1, shape2 = arbiter.shapes
    body1, body2 = shape1.body, shape2.body
    collided_bodies.append(body1)
    collided_bodies.append(body2)
    print(f"Collision detected between {body1} and {body2}")
    return True


collision_handler = space.add_collision_handler(1, 1)
collision_handler.begin = begin_collision

collision_handler_static_kinematic = space.add_collision_handler(0, 1)
collision_handler_static_kinematic.begin = begin_collision


def post_step(space, dt):
    global collided_bodies
    for body in collided_bodies:
        if body.body_type == 1:
            change_body_type(space, body, 'dynamic')
            print(collided_bodies)
            print('changed body_type for', body)
    collided_bodies.clear()


structs = [
    np.array([
        (1, 1),
        (1, 1)
    ]),
    np.array([
        (1, 1, 1, 1)
    ]),
    np.array([
        (1, 1),
        (1, 0),
        (1, 0),
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
    body = pymunk.Body(16, 100, body_type=pymunk.Body.KINEMATIC)
    body.velocity = (0, 20)
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
                shape.collision_type = 1
                shape.density = 3
                shape.elasticity = 0.075
                shape.friction = 0.75
                shape.color = (*color, 255)
                space.add(shape)
                shapes.append(shape)

    return shapes


def change_body_velocity(space, body, velocity: tuple):
    """
    :param space: select pymunk space
    :param body: select pymunk kinematic body
    :param velocity: tuple velocity
    """
    if body.body_type == pymunk.Body.KINEMATIC:
        body.velocity = velocity


def create_ground(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (0, 550), (800, 550), 5)
    shape.elasticity = 0.1
    shape.friction = 0.7
    shape.collision_type = 0
    space.add(body, shape)


create_ground(space)

for body in space.bodies:
    print(body, body.body_type)

def main():
    draw_options = pymunk.pygame_util.DrawOptions(display)
    draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    while True:
        last_body = space.bodies[-1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                struct = random.choice(structs)
                color = tuple(random.randrange(20, 236) for i in range(3))
                create_shape_from_struct(space, struct, color=color)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if last_body.body_type == 1:
                    last_body.angle += math.pi / 2

        display.fill((200, 200, 200))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            if last_body.body_type == 1:
                change_body_velocity(space, last_body, (0, 140))
        else:
            if last_body.body_type == 1:
                change_body_velocity(space, last_body, (0, 20))

        if keys[pygame.K_LEFT]:
            if last_body.body_type == 1:
                change_body_velocity(space, last_body, (-90, 0))

        if keys[pygame.K_RIGHT]:
            if last_body.body_type == 1:
                change_body_velocity(space, last_body, (90, 0))

        space.debug_draw(draw_options)
        space.step(1 / FPS)
        post_step(space, 1 / FPS)
        pygame.display.flip()
        clock.tick(FPS)


main()
pygame.quit()
