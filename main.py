import pyglet

from GLOBAL import *
from Game.Player import Player

sprites = pyglet.image.load("Doux.png")
sprites = pyglet.image.ImageGrid(sprites, 1, 24)
for image in sprites:
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

player = Player(sprites, 300, 300, 0, batch=NEAREST_BATCH, size=(200, 200))
CAMERA.object = player
GAME_MANAGER.add_object(player)

# тестовые платформы
platform1 = pymunk.Segment(PYMUNK_SPACE.static_body, (0, 0), (529, 0), 20)
platform1.collision_type = PLATFORM_COLLISION
PYMUNK_SPACE.add(platform1)

APP.run()