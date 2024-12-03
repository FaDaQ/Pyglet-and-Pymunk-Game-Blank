import pyglet
import pymunk

from Base import GameManager
from Base.GameApp import GameApp
from Game.Camera import Camera

PYMUNK_SPACE = pymunk.Space()
PYMUNK_SPACE.gravity = 0, -999
PYMUNK_SPACE.damping = 0.1

MAIN_BATCH = pyglet.graphics.Batch()
APP = GameApp(MAIN_BATCH, PYMUNK_SPACE, vsync=False, fps=144)
CAMERA = Camera(APP)
GAME_MANAGER = GameManager(APP, CAMERA)

KEYS = pyglet.window.key.KeyStateHandler()
APP.push_handlers(KEYS)


PLAYER_COLLISION = 1
PLATFORM_COLLISION = 2

# ПЕРЕЧСИЛЕНИЯ СОБЫТИЙ ОКНА (пока что никак не реализовано)
KEY_PRESSED = 1
KEY_JUST_PRESSED = 2

KEY_RELEASED = 3

MOUSE_PRESSED = 4
MOUSE_RELEASED = 5
MOUSE_MOTION = 6
MOUSE_DRAG = 7