import pyglet

from Components import Component


class Animator2D(Component):
    def __init__(self, game_object, image_grid: pyglet.image.ImageGrid = None, sections: dict[str, tuple[int, int]] = None,
                 animation_speed: float = 5):
        super().__init__(game_object)
        self.name = "Animator2D"

        self.__image_grid = image_grid
        self.__sections = sections
        self.animation_speed = animation_speed
        self.current_frame_index = 0
        self.current_frame = list(self.__sections.values())[0] if self.__sections is not None else None

        self.current_state = None
        self.running = False

    def update(self, dt):
        if self.running:
            animation_region = self.images[
                               self.__sections[self.current_state][0]
                               :
                               self.__sections[self.current_state][1]
                               ]

            if self.current_frame_index + dt * self.animation_speed < len(animation_region):
                self.current_frame_index += dt * self.animation_speed
            else:
                self.current_frame_index = 0

            if self.__sections and self.__image_grid:
                self.current_frame = animation_region[int(self.current_frame_index)]
                self.gameObject.image = self.current_frame

    def update_state(self, new_state):
        self.current_state = new_state
        if self.current_state != new_state:
            self.current_frame_index = 0

    def update_sections(self, new_sections: dict[object, tuple[int, int]]):
        self.__sections = new_sections

    def update_image_grid(self, new_image_grid: pyglet.image.ImageGrid):
        self.__image_grid = new_image_grid

    @property
    def sections(self):
        return self.__sections

    @property
    def images(self):
        return self.__image_grid
