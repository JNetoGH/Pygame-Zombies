import pygame
from pygame import Vector2, Surface, Color, Rect
from JNeto_engine_lite import constants


# =====================================================================================================================
# =====================================================================================================================

class Component:

    def __init__(self, name: str):
        self.name = name.capitalize()

    def update(self, game_object) -> None:
        pass

    def render_gizmos(self, game_surface: Surface) -> None:
        pass


# =====================================================================================================================
# =====================================================================================================================


class Transform(Component):
    def __init__(self):
        super().__init__("Transform")
        self.__position: Vector2 = Vector2(0, 0)
        self.angle: float = 0

    def get_position_copy(self) -> Vector2:
        # has to be a copy because Vector2 is a class, therefore, is passed as refenrence
        return self.__position.copy()

    def move_position(self, position: Vector2) -> None:
        self.__position = position

    def render_gizmos(self, game_surface: Surface) -> None:
        pygame.draw.circle(game_surface, Color("white"), self.__position, 5)


# ----------------------------------------------------------------------------------------------------------------------


class Sprite(Component):
    def __init__(self, image_path):
        super().__init__("Sprite")

        # image
        self.image_path = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.buffered_original_image: Surface = self.image.copy()
        self.scale = 1

        # image rect
        self.image_rect: Rect = self.image.get_rect()

        # gizmos
        self.color = constants.RED_PASTEL
        self.label_text_render = constants.MY_FONT.render("sprite rect", True, self.color, None)

    def change_image(self, image_path: str) -> None:
        self.image = pygame.image.load(image_path).convert_alpha()

    def scale_image(self, scale) -> None:
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale)).convert_alpha()
        self.scale = scale

    def rotate_image(self, angle) -> None:
        self.image = pygame.transform.rotate(self.buffered_original_image, angle)
        self.scale_image(self.scale)

    def render_gizmos(self, game_surface: Surface) -> None:
        pygame.draw.rect(game_surface, self.color, self.image_rect, 2)
        pos = (self.image_rect.x, self.image_rect.y - constants.FONT_SIZE - 10)
        game_surface.blit(self.label_text_render, pos)


# ----------------------------------------------------------------------------------------------------------------------


class Collider(Component):
    def __init__(self, offset_from_game_object_x, offset_from_game_object_y, width, height):
        super().__init__("Collider")

        # rect
        self.width = width
        self.height = height
        self.offset_from_game_object_x = offset_from_game_object_x
        self.offset_from_game_object_y = offset_from_game_object_y
        self.__inner_rect: Rect = Rect(0, 0, self.width, self.height)

        # gizmos
        self.WIDTH = 2
        self.color = constants.ORANGE_PASTEL
        self.label_text_render = constants.MY_FONT.render("Collider", True, self.color, None)

    def update(self, game_object) -> None:
        self.__realign_with_game_object_owner(game_object)

    def __realign_with_game_object_owner(self, game_object) -> None:
        # updates just in case they get changed in the middle of the game
        self.__inner_rect.width = self.width
        self.__inner_rect.height = self.height
        # I have to round it, because pygame is stupid and only treats rects with in variables so, a 50.9 position,
        # would be truncate to 50, removing the decimal part completely,  by rounding it I make 4.8 = 5, 3.2 => 3,
        # still not perfect, you can see little gaps but is way better than if I haven't done anything
        self.__inner_rect.centerx = round(game_object.transform.get_position_copy().x + self.offset_from_game_object_x)
        self.__inner_rect.centery = round(game_object.transform.get_position_copy().y + self.offset_from_game_object_y)

    def render_gizmos(self, game_surface: Surface) -> None:
        pygame.draw.rect(game_surface, self.color, self.__inner_rect, self.WIDTH)
        pos = (self.__inner_rect.x, self.__inner_rect.y + self.__inner_rect.height + 5)
        game_surface.blit(self.label_text_render, pos)


# ----------------------------------------------------------------------------------------------------------------------


class KeyTracker(Component):

    def __init__(self, pygame_key_code):
        super().__init__("KeyTracker")
        self.pygame_key_code = pygame_key_code
        self.total_times_fired: int = 0
        self.__has_key_been_fired_at_this_frame = False
        self.__has_key_been_released_at_this_frame = False
        self.__has_key_been_already_fired_but_not_released = False

    @property
    def has_key_been_released_at_this_frame(self):
        return self.__has_key_been_released_at_this_frame

    @property
    def has_key_been_fired_at_this_frame(self):
        return self.__has_key_been_fired_at_this_frame

    @property
    def is_key_being_held_down(self):
        return pygame.key.get_pressed()[self.pygame_key_code]

    def reset_total_times_fired(self) -> None:
        self.total_times_fired = 0

    def update(self, game_object) -> None:
        self.__has_key_been_fired_at_this_frame = False
        self.__has_key_been_released_at_this_frame = False
        if self.is_key_being_held_down and not self.__has_key_been_already_fired_but_not_released and not self.__has_key_been_fired_at_this_frame:
            self.__has_key_been_fired_at_this_frame = True
            self.total_times_fired += 1
            self.__has_key_been_already_fired_but_not_released = True
        if self.__has_key_been_already_fired_but_not_released and not self.is_key_being_held_down:
            self.__has_key_been_already_fired_but_not_released = False
            self.__has_key_been_released_at_this_frame = True
