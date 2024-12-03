from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Base.GameObject import GameObject


class Component:
    def __init__(self, game_object: 'GameObject'):
        self.name = "Default Component"
        self.gameObject = game_object

    def update(self, dt):
        pass

    def fixed_update(self, dt):
        pass

    name: str
    gameObject: 'GameObject'