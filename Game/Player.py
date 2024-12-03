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
from GLOBAL import APP, CAMERA, PYMUNK_SPACE, KEYS

def get_axis(neg, pos):
    return int(pos) - int(neg)

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
        self.body.add_shape(pymunk.Poly.create_box(self.body, (size[0]-80, size[1]-50)))

        # настраиваем и запускаем анимацию
        self.animator: Animator2D = self.add_component(Animator2D(self))
        if isinstance(img, ImageGrid):
            for image in img:
                image.anchor_x = image.width // 2
                image.anchor_y = image.height // 2
            self.animator.update_image_grid(img)
            self.animator.update_sections({
                "idle": (0, 4),
                "run": (5, 10),
                "crouch": (17, 18)
            })
            self.animator.update_state("idle")
            self.animator.running = True

        original_width = img[0].width if isinstance(img, ImageGrid) else img.width
        original_height = img[0].height if isinstance(img, ImageGrid) else img.height

        self.scale_x = size[0] / original_width
        self.scale_y = size[1] / original_height

        self.speed = 250


    def update(self, x: float | None = None, y: float | None = None, z: float | None = None,
               rotation: float | None = None, scale: float | None = None,
               scale_x: float | None = None, scale_y: float | None = None, dt=None) -> None:
        super().update(x, y, z, rotation, scale, scale_x, scale_y, dt)
        self.move(dt)

    def move(self, dt):
        self.body.velocity = pymunk.Vec2d(
            get_axis(KEYS[key.A], KEYS[key.D]) * self.speed,
            self.body.velocity.y
        )
