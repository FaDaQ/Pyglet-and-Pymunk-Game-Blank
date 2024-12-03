import math
import pymunk
from Components import Component


class PhysicsBody2D(Component, pymunk.Body):
    def __init__(self, game_object, space, body_type=pymunk.Body.DYNAMIC, mass=0.5, moment=float("inf")):
        Component.__init__(self, game_object)
        pymunk.Body.__init__(self, mass, moment, body_type)

        self.name = "PhysicsBody2D"
        self.position = (game_object.position[0], game_object.position[1])
        space.add(self)

    def add_shape(self, shape: pymunk.Shape):
        shape.body = self
        self.space.add(shape)

    def update(self, dt):
        self.gameObject.position = (self.position.x, self.position.y, 0)
        self.gameObject.rotation = -math.degrees(self.angle)