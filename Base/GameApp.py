import pyglet
from pyglet.gl import *
import pymunk.pyglet_util

draw_options = pymunk.pyglet_util.DrawOptions()

class GameApp(pyglet.window.Window):
    def __init__(self,
                 main_batch: pyglet.graphics.Batch, linear_batch: pyglet.graphics.Batch, nearest_batch: pyglet.graphics.Batch,
                 space: pymunk.Space,
                 width=1280, height=720, title="Pyglet - GameApp",
                 fps=999,
                 **kwargs):
        super().__init__(width, height, caption=title, **kwargs)

        self.space = space
        self.game_manager = None

        self.__batch = main_batch
        self.__linear_batch = linear_batch
        self.__nearest_batch = nearest_batch

        self.__max_fps = fps
        self.__fixed_update_fps = 360


    def on_draw(self):
        self.clear()

        self.space.debug_draw(draw_options)
        self.__batch.draw()

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        self.__linear_batch.draw()

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.__nearest_batch.draw()




    def update(self, dt):
        if self.game_manager is not None:
            self.game_manager.update(dt)

    def fixed_update(self, dt):
        self.space.step(dt)
        if self.game_manager is not None:
            self.game_manager.fixed_update(dt)

    def on_mouse_press(self, x, y, button, modifiers):
        # Получаем реальные координаты мыши с учётом смещения камеры
        mouse_x = x - self.game_manager.camera.scroll_x
        mouse_y = y - self.game_manager.camera.scroll_y

        # Спавним круг с учётом смещения камеры
        shape = pymunk.Circle(self.space.static_body, 40, (mouse_x, mouse_y))
        shape.collision_type = 2
        self.space.add(shape)

    @property
    def batch(self):
        return self.__batch

    def run(self):
        pyglet.clock.schedule(self.update)
        pyglet.clock.schedule_interval(self.fixed_update, 1 / self.__fixed_update_fps)
        pyglet.app.run(interval=1 / self.__max_fps)