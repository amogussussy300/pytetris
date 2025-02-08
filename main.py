import math
import os
import pygame
import pymunk
import numpy as np
import random
import pymunk.pygame_util

resolution = (800, 800)
display = pygame.display.set_mode(resolution, pygame.SRCALPHA)
clock = pygame.time.Clock()
FPS = 144
collided_bodies = []
space = pymunk.Space()
space.gravity = 0, 850
air_friction = 0.369420228
pygame.init()
font = pygame.font.SysFont('Aerial', 36)
font_color = (100, 0, 0)


class CustomDrawOptions(pymunk.pygame_util.DrawOptions):
    def draw_circle(self, *args):
        if len(args) == 6:
            pos, angle, radius, outline_color, fill_color, shape = args
        else:
            return

        if shape.collision_type == 3:
            return
        super().draw_circle(*args)


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

def begin_finishline_collision(arbiter, sp, data):
    return False


collision_handler = space.add_collision_handler(1, 1)
collision_handler.begin = begin_collision

collision_handler_static_kinematic = space.add_collision_handler(0, 1)
collision_handler_static_kinematic.begin = begin_collision

collision_handler_wind_kinematic = space.add_collision_handler(1, 3)
collision_handler_wind_kinematic.begin = begin_w_kinematic

collision_handler_finish_line1 = space.add_collision_handler(5, 1)
collision_handler_finish_line1.begin = begin_finishline_collision

collision_handler_finish_line2 = space.add_collision_handler(5, 2)
collision_handler_finish_line2.begin = begin_finishline_collision

collision_handler_finish_line3 = space.add_collision_handler(5, 3)
collision_handler_finish_line3.begin = begin_finishline_collision

collision_handler_finish_line4 = space.add_collision_handler(5, 0)
collision_handler_finish_line4.begin = begin_finishline_collision


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
        (0, 1),
        (1, 1),
        (1, 0)
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
    shape = pymunk.Circle(body, 1)
    shape.friction = air_friction
    shape.elasticity = 0
    shape.collision_type = 3
    shape.color = (200, 200, 200, 255)
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


def create_puzzle_ground(sp, camera_offset, segment_width=20, segment_height=20, gap_probability=0.45):
    start_x = resolution[0] // 3 + 40
    end_x = resolution[0] - resolution[0] // 3 - 40
    start_y = resolution[1] - camera_offset
    end_y = resolution[1] + camera_offset
    ground_length = end_x - start_x
    ground_height = end_y - start_y
    num_segments_x = int(ground_length // segment_width)
    num_segments_y = int(ground_height // segment_height)

    segment_grid = np.zeros((num_segments_y, num_segments_x), dtype=bool)

    for j in range(num_segments_y):
        for i in range(num_segments_x):
            if j == 0 or (segment_grid[j - 1, i] and not segment_grid[j, i]):
                if np.random.random() > gap_probability:
                    segment_x = start_x + i * segment_width
                    segment_y = start_y + j * segment_height

                    body = pymunk.Body(body_type=pymunk.Body.STATIC)

                    vertices = [
                        (segment_x, segment_y),
                        (segment_x + segment_width, segment_y),
                        (segment_x + segment_width, segment_y + segment_height),
                        (segment_x, segment_y + segment_height),
                    ]

                    shape = pymunk.Poly(body, vertices)
                    shape.elasticity = 0.1
                    shape.friction = 0.7
                    shape.collision_type = 0
                    shape.color = (255, 255, 255, 0)

                    sp.add(body, shape)

                    segment_grid[j, i] = True



def end_screen(result):
    while True:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                from MainWindow import mainWindow
                mainWindow()
                pygame.quit()
                return

        display.fill((0, 0, 0, 50))
        large_font = pygame.font.SysFont('comicsans', 80)
        continue_font = pygame.font.SysFont('comicsans', 55)
        last_score = large_font.render('Score: ' + str(result["final_score"]), 1,
                                     (255, 255, 255))
        continue_text = continue_font.render('Click to continue', 1, (200, 200, 200))
        display.blit(last_score, (resolution[0] / 2 - last_score.get_width() / 2, resolution[1] // 4))
        display.blit(continue_text, (resolution[0] / 2 - continue_text.get_width() / 2, resolution[1] // 2))
        pygame.display.update()


# game_type 1 -- оригинальный
# game_type 2 -- выживание
# game_type 3 -- пазл


def draw_finish_line(sp):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    shape = pymunk.Poly(body, ((0, 15),
                               (resolution[0], 15),
                               (resolution[0], 30),
                               (0, 30)))
    shape.elasticity = 0
    shape.friction = 0
    shape.collision_type = 5
    shape.color = (45, 45, 45, 0)
    shape.sensor = True
    sp.add(body, shape)
    body.velocity = (0, 0)



def main(WIND: bool, game_type: int, res=None):
    global resolution
    global font
    global font_color
    reset_game_state()
    if res is not None:
        resolution = res

    if game_type == 1:
        counter = 5
        result = {
            "highest_block": 0,
            "amount_of_fallen_blocks": 0,
            "final_score": 0
        }
        fallen_blocks = 0

    if game_type == 2:
        TIMER_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMER_EVENT, 1000)
        counter = 240
        image = pygame.image.load('hp_heart.png').convert_alpha()
        health_point = pygame.transform.scale(image, (30, 30))
        result = {
            "highest_block": 0,
            "amount_of_fallen_blocks": 0,
            "final_score": 0
        }
        fallen_blocks = 0

    if game_type == 3:
        fallen_blocks = 0
        result = {
            "amount_of_blocks": 0,
            "amount_of_fallen_blocks": 0,
            "final_score": 0
        }
        draw_finish_line(space)

    camera = pygame.Vector2(0, -59.3)
    draw_options = CustomDrawOptions(display)
    draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    if game_type != 3:
        create_ground(space, abs(camera.y))
    else:
        create_puzzle_ground(space, abs(camera.y))
    while True:
        if game_type == 1:
            if counter < 0:
                rhby = resolution[1] - highest_dynamic_body
                result["highest_block"] = rhby
                result["amount_of_fallen_blocks"] = fallen_blocks
                if not WIND:
                    result["final_score"] = round(rhby - fallen_blocks * (fallen_blocks ** 0.5)) if (rhby - fallen_blocks >= 0) else 0
                else:
                    result["final_score"] = round(rhby - fallen_blocks) if (rhby - fallen_blocks >= 0) else 0
                for element in bodies:
                    remove_body(space, element[3].body)
                highest_body_y_b = 0
                highest_body_y = 0
                t_bodies.clear()
                b_bodies.clear()
                new_bodies.clear()
                last_body = None
                end_screen(result)
        bodies = [(shape.bb.top, shape.bb.bottom, shape.body, shape) for shape in space.shapes
                  if shape.body.body_type != pymunk.Body.STATIC and shape.friction != air_friction and shape.collision_type != 5]
        t_bodies = [position[0] for position in bodies]
        b_bodies = [position[1] for position in bodies]
        s_bodies = [(shape.bb.top, shape.bb.bottom, shape.body, shape) for shape in space.shapes if
                    shape.friction != air_friction and shape.collision_type != 5]
        new_bodies = [i[2] for i in s_bodies]
        w_bodies = [(shape.bb.top, shape.bb.bottom, shape.body, shape) for shape in space.shapes if shape.friction == air_friction]
        dynamic_bodies = [i[1] for i in s_bodies if i[2].body_type == pymunk.Body.DYNAMIC]
        if game_type == 3:
            finish_line = [(shape.bb.top, shape.bb.bottom, shape.body, shape) for shape in space.shapes if shape.collision_type == 5]
            finish_line[0][2].position = (0, resolution[1] - resolution[1] // 3 - 35)
            finish_line[0][2].velocity = (0, 1000 * fallen_blocks)
        if t_bodies:
            highest_body_y = min(t_bodies)
            highest_body_y_b = min(b_bodies)
        else:
            highest_body_y = 59.3
            highest_body_y_b = 0
        if dynamic_bodies:
            highest_dynamic_body = min(dynamic_bodies)
            lowest_dynamic_body = max(dynamic_bodies)
        else:
            highest_dynamic_body = resolution[1]
            lowest_dynamic_body = resolution[1]
        last_body = new_bodies[-1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                struct = random.choice(structs)
                if last_body.body_type != pymunk.Body.KINEMATIC:
                    color = tuple(random.randrange(25, 231) for _ in range(3))
                    font_color = color
                if last_body.body_type != pymunk.Body.KINEMATIC:
                    if last_body.body_type == pymunk.Body.STATIC:
                        create_shape_from_struct(space, struct, position=(resolution[0] // 2, highest_body_y + 10), color=(*color, 255))
                        if game_type == 1:
                            counter -= 1
                    else:
                        if (resolution[1] - highest_body_y) > resolution[1] - 160:
                            create_shape_from_struct(space, struct, position=(resolution[0] // 2, highest_body_y - 250), color=(*color, 255))
                            if game_type == 1:
                                counter -= 1
                        else:
                            create_shape_from_struct(space, struct, position=(resolution[0] // 2, highest_body_y - highest_body_y_b), color=(*color, 255))
                            if game_type == 1:
                                counter -= 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if last_body.body_type == 1:
                    last_body.angle += math.pi / 2
            if game_type == 2:
                if event.type == TIMER_EVENT:
                    counter -= 1

        for element in bodies:
            if (element[0] - (element[0] - element[1]) * 3) > (resolution[1] + (element[0] - element[1])):
                block_under_0_event(element[3])
                fallen_blocks += 1
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
                if element[0] > lowest_dynamic_body + 5:
                    remove_body(space, element[3].body)
                if element[2].velocity[0] < 4 and element[2].velocity[1] < 4:
                    remove_body(space, element[3].body)

        display.fill((155, 155, 155))
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

        if game_type == 1:
            if counter >= 0:
                text_surface = font.render(f"{counter}", True, font_color)
                draw_options.surface.blit(text_surface, (resolution[0] - 40, 15))
        elif game_type == 2:
            if counter >= 0:
                text_surface = font.render(f"{counter}", True, font_color)
                draw_options.surface.blit(text_surface, (resolution[0] - 50, 25))
            if fallen_blocks < 2:
                for i in range(1, (4 - fallen_blocks)):
                    draw_options.surface.blit(health_point, (45 * i, 25))
            if fallen_blocks > 2 or counter <= 0:
                print('yes')
                rhby = resolution[1] - highest_dynamic_body
                result["highest_block"] = rhby
                result["amount_of_fallen_blocks"] = fallen_blocks
                result["final_score"] = round(rhby - fallen_blocks) + len(dynamic_bodies) * 2
                for element in bodies:
                    remove_body(space, element[3].body)
                highest_body_y_b = 0
                highest_body_y = 0
                t_bodies.clear()
                b_bodies.clear()
                new_bodies.clear()
                last_body = None
                end_screen(result)
        elif game_type == 3:
            if highest_dynamic_body <= (finish_line[0][2].position[1] + 15.1) and len(dynamic_bodies) > 0:
                rhby = len(dynamic_bodies)
                result["amount_of_blocks"] = rhby
                result["amount_of_fallen_blocks"] = fallen_blocks
                result["final_score"] = rhby * 10 - fallen_blocks * 2
                for element in bodies:
                    remove_body(space, element[3].body)
                remove_body(space, finish_line[0][2])
                highest_body_y_b = 0
                highest_body_y = 0
                t_bodies.clear()
                b_bodies.clear()
                new_bodies.clear()
                finish_line.clear()
                last_body = None
                end_screen(result)

        pygame.display.flip()
        clock.tick(FPS)


def reset_game_state():
    global space, collided_bodies
    space = pymunk.Space()
    space.gravity = (0, 850)
    collided_bodies = []
    collision_handler = space.add_collision_handler(1, 1)
    collision_handler.begin = begin_collision

    collision_handler_static_kinematic = space.add_collision_handler(0, 1)
    collision_handler_static_kinematic.begin = begin_collision

    collision_handler_wind_kinematic = space.add_collision_handler(1, 3)
    collision_handler_wind_kinematic.begin = begin_w_kinematic
