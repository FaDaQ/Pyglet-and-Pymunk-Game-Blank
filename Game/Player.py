import enum
from math import copysign

import pyglet
import pymunk
from pyglet.gl import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.image import AbstractImage, Animation, ImageGrid
from pyglet.window import key

from Base import GameObject
from Components import PhysicsBody2D
from Components.Animator2D import Animator2D
from Game.Camera import Camera
from GLOBAL import APP, CAMERA, PYMUNK_SPACE, KEYS, PLAYER_COLLISION, PLATFORM_COLLISION


def get_axis(neg, pos):
    return int(pos) - int(neg)

def normalize_direction(x):
    # Если x не равен 0, приводим его к -1 или 1
    return copysign(1, x) if x != 0 else 0

class PlayerState(enum.Enum):
    IDLE = 0
    RUN = 1
    CROUCH = 2
    FALLING = 3
    SITTING = 4


class Player(GameObject):
    def __init__(self,
                 img: AbstractImage | Animation | ImageGrid,
                 x: float = 0, y: float = 0, z: float = 0,
                 blend_src: int = GL_SRC_ALPHA,
                 blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
                 batch: Batch | None = None,
                 group: Group | None = None,
                 subpixel: bool = False,
                 program: ShaderProgram | None = None,
                 size: tuple[float, float] = (100, 100)) -> None:
        super().__init__(img, x, y, z,
                         blend_src, blend_dest,
                         batch, group,
                         subpixel, program)

        self.body: PhysicsBody2D = self.add_component(PhysicsBody2D(self, PYMUNK_SPACE))
        self.shape = pymunk.Poly.create_box(self.body, (size[0]-80, size[1]-50))
        self.shape.collision_type = PLAYER_COLLISION
        self.body.add_shape(self.shape)


        self.grounded_handler = PYMUNK_SPACE.add_collision_handler(PLAYER_COLLISION, PLATFORM_COLLISION)
        self.grounded_handler.begin = self.grounded_collision_handler

        self.falling_handler = PYMUNK_SPACE.add_collision_handler(PLAYER_COLLISION, PLATFORM_COLLISION)
        self.falling_handler.separate = self.falling_collision_handler

        self.state = PlayerState.IDLE
        # настраиваем и запускаем анимацию
        self.animator: Animator2D = self.add_component(Animator2D(self))
        self.animator.animation_speed = 10
        if isinstance(img, ImageGrid):
            for image in img:
                image.anchor_x = image.width // 2
                image.anchor_y = image.height // 2
            self.animator.update_image_grid(img)
            self.animator.update_sections({
                PlayerState.IDLE: (0, 4),
                PlayerState.RUN: (5, 10),
                PlayerState.SITTING: (17, 18),
                PlayerState.CROUCH: (17, 24),
            })
            self.animator.update_state(self.state)
            self.animator.running = True

        original_width = img[0].width if isinstance(img, ImageGrid) else img.width
        original_height = img[0].height if isinstance(img, ImageGrid) else img.height

        self.scale_x = size[0] / original_width
        self.scale_y = size[1] / original_height

        self.speed = 350

        self.grounded = False
        self.max_jumps = 2
        self.remaining_jumps = 0
        self.jump_strength = 1500


    def update(self, x: float | None = None, y: float | None = None, z: float | None = None,
               rotation: float | None = None, scale: float | None = None,
               scale_x: float | None = None, scale_y: float | None = None, dt=None) -> None:
        super().update(x, y, z, rotation, scale, scale_x, scale_y, dt)
        self.move(dt)

    def move(self, dt):
        if self.state == PlayerState.FALLING:
            self.animator.running = False

        self.body.velocity = pymunk.Vec2d(
            get_axis(KEYS.is_pressed(key.A), KEYS.is_pressed(key.D)) * self.speed,
            self.body.velocity.y
        )

        if self.body.velocity.x != 0:
            self.state = PlayerState.RUN
            if normalize_direction(self.body.velocity.x) < 0:
                self.scale_x = -abs(self.scale_x)
            else:
                self.scale_x = abs(self.scale_x)
            self.animator.update_state(self.state)
        else:
            self.state = PlayerState.IDLE
            self.animator.update_state(self.state)

        if KEYS.is_pressed_once(key.SPACE):
            self.jump()

        if KEYS.is_pressed(key.LCTRL):
            self.crouch()

    def jump(self):
        if self.grounded or self.remaining_jumps > 0:
            self.body.velocity = (self.body.velocity.x, self.jump_strength)
            self.grounded = False
            self.remaining_jumps -= 1
            self.state = PlayerState.FALLING

    def crouch(self):
        match self.state:
            case PlayerState.IDLE:
                self.state = PlayerState.SITTING
            case PlayerState.RUN:
                self.state = PlayerState.CROUCH
            case PlayerState.FALLING:
                self.state = PlayerState.SITTING

        self.animator.update_state(self.state)
        self.animator.running = True

    def grounded_collision_handler(self, arbiter, space, data):
        if self.body.velocity.y < 0:
            self.grounded = True
            self.remaining_jumps = self.max_jumps
            self.body.velocity = pymunk.Vec2d(self.body.velocity.x, 0)
            self.state = PlayerState.IDLE
            self.animator.running = True

        return True

    def falling_collision_handler(self, arbiter, space, data):
        if self.body.velocity.y < 0:
            self.grounded = False
            self.remaining_jumps -= 1
            self.state = PlayerState.FALLING