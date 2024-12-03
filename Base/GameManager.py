import pyglet

from Base import GameApp
from Game.Camera import Camera

game_manager_is_set = False
class GameManager:
    def __init__(self, app: GameApp, camera: Camera):
        self.app = app
        self.game_objects = set()
        self.camera = camera

        if not game_manager_is_set:
            app.game_manager = self
        else:
            raise Exception("GameManager already initialized")

    def update(self, dt):
        self.camera.update(dt)
        self.camera.apply()
        [obj.update(dt=dt) for obj in self.game_objects]

    def fixed_update(self, dt):
        [obj.fixed_update(dt=dt) for obj in self.game_objects]

    def add_object(self, game_object):
        self.game_objects.add(game_object)


