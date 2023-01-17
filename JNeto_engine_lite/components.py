import pygame
from pygame import Vector2


# =====================================================================================================================
# =====================================================================================================================

class Component:

    def __init__(self, name: str):
        self.name = name.capitalize()

    def update(self):
        pass


# =====================================================================================================================
# =====================================================================================================================


class Transform(Component):
    def __init__(self):
        super().__init__("Transform")
        self.__position: Vector2 = Vector2(0, 0)
        self.angle: float = 0

    # has to be a copy because Vector2 is a class, therefore, is passed as refenrence
    def get_position_copy(self) -> Vector2:
        return self.__position.copy()

    def set_position(self, position: Vector2) -> None:
        self.__position = position

# ---------------------------------------


class Sprite(Component):
    def __init__(self, image_path):
        super().__init__("Sprite")
        self.image_path = pygame.image.load(image_path).convert_alpha()
        self.image: pygame.Surface = pygame.image.load(image_path).convert_alpha()
        self.image_rect: pygame.Rect = self.image.get_rect()

    def change_image(self, image_path: str) -> None:
        self.image = pygame.image.load(image_path).convert_alpha()

    def scale_image(self, scale) -> None:
        if self.image is not None:
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale,
                                                             self.image.get_height() * scale)).convert_alpha()

# ---------------------------------------


class Merda(Component):

    def __init__(self):
        super().__init__("Merda")

    def update(self):
        print("caralho")