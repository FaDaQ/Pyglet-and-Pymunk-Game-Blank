import pyglet
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from Base.GameApp import GameApp
    from Base.GameObject import GameObject

class Camera:
    def __init__(self, app: 'GameApp', offset: tuple[int, int] = (0, 0)):
        self.app = app
        self.screen_width, self.screen_height = app.width, app.height
        self.offset_x, self.offset_y = offset
        self.scroll_x, self.scroll_y = 0, 0

        self.object: 'GameObject' = None

    def update(self, dt):
        # print(self.scroll_x, self.scroll_y)
        if self.object is not None:
            # Учитываем центр объекта для корректного позиционирования
            object_x = self.object.position[0] + self.object.image.width // 2
            object_y = self.object.position[1] + self.object.image.height // 2

            # Вычисляем смещение камеры
            self.scroll_x = (self.screen_width / 2) - object_x
            self.scroll_y = (self.screen_height / 2) - object_y

    def apply(self):
        self.app.view = pyglet.math.Mat4() # обнуляем матрицу вида, иначе камера будет бесконечно смещаться
        self.app.view = self.app.view.translate(pyglet.math.Vec3(self.scroll_x, self.scroll_y, 0))
        pass

    def reset(self):
        self.scroll_x = 0
        self.scroll_y = 0
        self.object: 'GameObject' = None
        self.app.view.translate(pyglet.math.Vec3(self.scroll_x, self.scroll_y, 0))
