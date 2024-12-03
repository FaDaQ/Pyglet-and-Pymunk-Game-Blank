import pyglet
from pyglet.gl import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.graphics.shader import ShaderProgram
from pyglet.graphics import Batch, Group
from pyglet.image import AbstractImage, Animation

from Components import Component


class GameObject(pyglet.sprite.Sprite):
    def __init__(self,
                 img: AbstractImage | Animation,
                 x: float = 0, y: float = 0, z: float = 0,
                 blend_src: int = GL_SRC_ALPHA,
                 blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
                 batch: Batch | None = None,
                 group: Group | None = None,
                 subpixel: bool = False,
                 program: ShaderProgram | None = None) -> None:
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        super().__init__(img, x, y, z,
                         blend_src, blend_dest,
                         batch, group,
                         subpixel, program)


        self.components: set[Component] = set()

    def update(self, x: float | None = None, y: float | None = None, z: float | None = None,
               rotation: float | None = None, scale: float | None = None,
               scale_x: float | None = None, scale_y: float | None = None, dt=None) -> None:
        super().update(x, y, z, rotation, scale, scale_x, scale_y)
        [component.update(dt) for component in self.components] # update all components

    def fixed_update(self, x: float | None = None, y: float | None = None, z: float | None = None,
               rotation: float | None = None, scale: float | None = None,
               scale_x: float | None = None, scale_y: float | None = None, dt=None) -> None:
        super().update(x, y, z, rotation, scale, scale_x, scale_y)
        [component.fixed_update(dt) for component in self.components]

    def add_component(self, component: Component):
        self.components.add(component)
        return component