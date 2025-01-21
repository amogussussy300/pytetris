import math
import pygame
import pymunk
import numpy as np
import random
import pymunk.pygame_util

resolution = (800, 600)
display = pygame.display.set_mode(resolution, pygame.SRCALPHA)
clock = pygame.time.Clock()
FPS = 144
collided_bodies = []
space = pymunk.Space()
space.gravity = 0, 850
air_friction = 0.369420228
pygame.init()

print('WIND??????????????????????? (y/n)')
print('WIND??????????????????????? (y/n)')
print('WIND??????????????????????? (y/n)')
print('WIND??????????????????????? (y/n)')
print('WIND??????????????????????? (y/n)')
prompt = input('WIND??????????????????????? (y/n): ')
if prompt.strip().lower() == 'y':
    WIND = True
elif prompt.strip().lower() == 'n':
    WIND = False
else:
    print(':(')
    exit()


def change_body_type(sp, body, b_type):
    """
    :param sp: select pymunk space
    :param body: select pymunk body
    :param b_type: select type: static, dynamic, kinematic
    """
    sp.remove(body)

    if b_type == 'static':
        body.body_type = pymunk.Body.STATIC
    elif b_type == 'dynamic':
        body.body_type = pymunk.Body.DYNAMIC
    elif b_type == 'kinematic':
        body.body_type = pymunk.Body.KINEMATIC
    else:
        raise ValueError("Body type is incorrect")

    sp.add(body)


def begin_collision(arbiter, sp, data):
    shape1, shape2 = arbiter.shapes
    body1, body2 = shape1.body, shape2.body
    change_body_velocity(sp, body1, (0, 0))
    change_body_velocity(sp, body2, (0, 0))
    collided_bodies.append(body1)
    collided_bodies.append(body2)
    return True


def begin_w_kinematic(arbiter, sp, data):
    return True


collision_handler = space.add_collision_handler(1, 1)
collision_handler.begin = begin_collision

collision_handler_static_kinematic = space.add_collision_handler(0, 1)
collision_handler_static_kinematic.begin = begin_collision

collision_handler_wind_kinematic = space.add_collision_handler(1, 3)
collision_handler_wind_kinematic.begin = begin_w_kinematic


def post_step(sp, dt):
    global collided_bodies
    for body in collided_bodies:
        if body.body_type == 1:
            change_body_type(sp, body, 'dynamic')
            print('changed body_type for', body)
    collided_bodies.clear()


structs = [
    np.array([
        (1, 1),
        (1, 1)
    ]),
    np.array([
        (1, 0),
        (1, 0),
        (1, 0),
        (1, 0)
    ]),
    np.array([
        (1, 1),
        (1, 0),
        (1, 0)
    ]),
    np.array([
        (1, 1),
        (0, 1),
        (0, 1)
    ]),
    np.array([
        (1, 0),
        (1, 1),
        (0, 1)
    ]),
    np.array([
        (1, 0),
        (1, 1),
        (0, 1)
    ]),
    np.array([
        (0, 1),
        (1, 1),
        (0, 1)
    ])
]


def create_shape_from_struct(sp, struct, position=(resolution[0] // 2, 0), cell_size=20, color=(255, 255, 255, 255)):
    body = pymunk.Body(16, 100, body_type=pymunk.Body.KINEMATIC)
    body.velocity = (0, 25)
    body.position = position
    sp.add(body)

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
                shape.color = color
                sp.add(shape)
                shapes.append(shape)

    return shapes


def create_wind_particle(sp, position, velocity=(500, 10), mass=40):
    body = pymunk.Body(mass, 56, body_type=pymunk.Body.DYNAMIC)
    body.velocity = velocity
    body.position = position
    shape = pymunk.Circle(body, 0.02)
    shape.friction = air_friction
    shape.elasticity = 0.5
    shape.collision_type = 3
    shape.color = (200, 200, 200, 0)
    sp.add(body, shape)


def change_body_velocity(sp, body, velocity: tuple):
    """
    :param sp: select pymunk space
    :param body: select pymunk kinematic body
    :param velocity: tuple velocity
    """
    if body.body_type == pymunk.Body.KINEMATIC:
        body.velocity = velocity


def remove_body(sp, body):
    for shape in body.shapes:
        if shape in sp.shapes:
            sp.remove(shape)

    constraints_to_remove = [
        constraint for constraint in sp.constraints
        if body in (constraint.a, constraint.b)
    ]
    for constraint in constraints_to_remove:
        sp.remove(constraint)

    if body in sp.bodies:
        sp.remove(body)


def block_under_0_event(block: pymunk.Shape):
    print('block under 0:', block, block.body.position)


def create_ground(sp, camera_offset):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Poly(body, ((resolution[0] // 3 + 40, resolution[1] - camera_offset),
                               (resolution[0] - resolution[0] // 3 - 40, resolution[1] - camera_offset),
                               (resolution[0] - resolution[0] // 3 - 40, resolution[1] + camera_offset),
                               (resolution[0] // 3 + 40, resolution[1] + camera_offset)))
    shape.elasticity = 0.1
    shape.friction = 0.7
    shape.collision_type = 0
    shape.color = (255, 255, 255, 0)
    sp.add(body, shape)


def main():
    camera = pygame.Vector2(0, -59.3)
    draw_options = pymunk.pygame_util.DrawOptions(display)
    draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    create_ground(space, abs(camera.y))
    while True:
        bodies = [(shape.bb.top, shape.bb.bottom, shape.body, shape) for shape in space.shapes
                  if shape.body.body_type != pymunk.Body.STATIC and shape.friction != air_friction]
        t_bodies = [position[0] for position in bodies]
        b_bodies = [position[1] for position in bodies]
        s_bodies = [(shape.bb.top, shape.bb.bottom, shape.body, shape) for shape in space.shapes if
                    shape.friction != air_friction]
        new_bodies = [i[2] for i in s_bodies]
        if WIND:
            w_bodies = [(shape.bb.top, shape.bb.bottom, shape.body, shape) for shape in space.shapes if shape.friction == air_friction]
            dynamic_bodies = [i[1] for i in s_bodies if i[2].body_type == pymunk.Body.DYNAMIC]
        if t_bodies:
            highest_body_y = min(t_bodies)
            highest_body_y_b = min(b_bodies)
        else:
            highest_body_y = 59.3
            highest_body_y_b = 0
        if WIND:
            if dynamic_bodies:
                highest_dynamic_body = min(dynamic_bodies)
            else:
                highest_dynamic_body = resolution[1]
        last_body = new_bodies[-1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                struct = random.choice(structs)
                color = tuple(random.randrange(25, 231) for _ in range(3))
                if last_body.body_type != pymunk.Body.KINEMATIC:
                    if last_body.body_type == pymunk.Body.STATIC:
                        create_shape_from_struct(space, struct, position=(resolution[0] // 2, highest_body_y + 10), color=(*color, 255))
                    else:
                        if (resolution[1] - highest_body_y) > resolution[1] - 160:
                            create_shape_from_struct(space, struct, position=(resolution[0] // 2, highest_body_y - 250), color=(*color, 255))
                        else:
                            create_shape_from_struct(space, struct, position=(resolution[0] // 2, highest_body_y - highest_body_y_b), color=(*color, 255))
                else:
                    change_body_type(space, last_body, 'dynamic')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if last_body.body_type == 1:
                    last_body.angle += math.pi / 2

        for element in bodies:
            if (element[0] - (element[0] - element[1]) * 3) > (resolution[1] + (element[0] - element[1])):
                block_under_0_event(element[3])
                remove_body(space, element[3].body)

        if WIND:
            w_pos = (random.randrange(-resolution[0], resolution[0]), random.randrange(-resolution[1], resolution[1]))
            w_v = (600, random.randrange(10, 90))
            create_wind_particle(space, w_pos, w_v, random.randrange(15, 135))

            for element in w_bodies:
                if (element[0] - (element[0] - element[1]) * 3) > (resolution[1] + (element[0] - element[1])):
                    remove_body(space, element[3].body)
                if len(w_bodies) > 120:
                    remove_body(space, w_bodies[-1][3].body)
                if element[0] > highest_dynamic_body + 40:
                    remove_body(space, w_bodies[w_bodies.index(element)][3].body)

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
                change_body_velocity(space, last_body, (-90, last_body.velocity[1]))

        if keys[pygame.K_RIGHT]:
            if last_body.body_type == 1:
                change_body_velocity(space, last_body, (90, last_body.velocity[1]))

        if last_body.body_type != pymunk.Body.STATIC and [i for i in last_body.shapes][0].friction != air_friction:
            if resolution[1] - (highest_body_y - 100) > resolution[1]:
                camera.y = -highest_body_y + (highest_body_y - (highest_body_y_b - 20))

        offset = pymunk.Transform(tx=0, ty=camera.y)
        space.step(1 / FPS)
        post_step(space, 1 / FPS)
        draw_options.transform = offset
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(FPS)


main()
pygame.quit()
