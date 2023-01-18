import pygame
from pygame import Vector2, Surface, Color, Rect
from pygame.font import Font
from engine_JNeto_LITE import constants


# =====================================================================================================================
# =====================================================================================================================

class Component:

    def __init__(self, name: str):
        self.name = name.capitalize()
        self.owner = None

    def update(self) -> None:
        pass

    def render_gizmos(self, game_surface: Surface) -> None:
        pass


# =====================================================================================================================
# =====================================================================================================================


class Transform(Component):
    def __init__(self):
        super().__init__("Transform")
        self.__position: Vector2 = Vector2(0, 0)

    def get_position_copy(self) -> Vector2:
        # has to be a copy because Vector2 is a class, therefore, is passed as refenrence
        return self.__position.copy()

    def move_position(self, new_position: Vector2) -> None:
        if not self.owner.has_collider_component:
            self.__position = new_position
            return
        if self.owner.scene is None:
            self.__position = new_position
            return

        collider: Collider = self.owner.collider_component
        if len(collider.collidable_classes) == 0:
            self.__position = new_position
            return

        for other in self.owner.scene.game_objects:
            if other == self.owner:
                continue
            if not other.__class__ in collider.collidable_classes:
                continue
            if not other.has_collider_component:
                continue

            # DX COLLISION
            projection_dx = collider.get_inner_rect_copy()
            projection_dx.centerx = new_position.x
            projection_dx.centery = self.__position.y
            if other.collider_component.is_there_overlap_with_rect(projection_dx):
                new_position.x = self.__position.x

            # DY COLLISION
            projection_dy = collider.get_inner_rect_copy()
            projection_dy.centerx = self.__position.x
            projection_dy.centery = new_position.y
            if other.collider_component.is_there_overlap_with_rect(projection_dy):
                new_position.y = self.__position.y

        self.__position = new_position

    def render_gizmos(self, game_surface: Surface) -> None:
        pygame.draw.circle(game_surface, Color("white"), self.__position, constants.GIZMOS_WIDTH*2)


# ----------------------------------------------------------------------------------------------------------------------


class Sprite(Component):
    def __init__(self, image_path):
        super().__init__("Sprite")

        # image
        self.image_path = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.buffered_original_image: Surface = self.image.copy()
        self.scale = 1
        self.angle = 0

        # image rect
        self.image_rect: Rect = self.image.get_rect()

        # gizmos
        self.color = constants.RED_PASTEL
        self.label_text_render = constants.MY_FONT.render("sprite", True, self.color, None)

    def change_image(self, image_path: str) -> None:
        self.image = pygame.image.load(image_path).convert_alpha()

    def scale_image(self, scale) -> None:
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale)).convert_alpha()
        self.buffered_original_image = \
            pygame.transform.scale(self.buffered_original_image,
                                   (self.buffered_original_image.get_width() * scale,
                                    self.buffered_original_image.get_height() * scale)).convert_alpha()
        self.scale = scale

    def rotate_image(self, angle) -> None:
        # check for performance
        if self.angle == angle:
            return
        self.angle = angle
        self.image = pygame.transform.rotate(self.buffered_original_image, self.angle)

    def render_gizmos(self, game_surface: Surface) -> None:
        pygame.draw.rect(game_surface, self.color, self.image_rect, constants.GIZMOS_WIDTH)
        pos = (self.image_rect.x, self.image_rect.y - constants.FONT_SIZE - 10)
        game_surface.blit(self.label_text_render, pos)


# ----------------------------------------------------------------------------------------------------------------------


class Collider(Component):
    def __init__(self, offset_from_game_object_x, offset_from_game_object_y, width, height):
        super().__init__("Collider")

        # this list holds all the GameObject subclasses that the owner of this collider can colide with
        self.collidable_classes = []

        # rect
        self.width = width
        self.height = height
        self.offset_from_game_object_x = offset_from_game_object_x
        self.offset_from_game_object_y = offset_from_game_object_y
        self.__inner_rect: Rect = Rect(0, 0, self.width, self.height)

        # gizmos
        self.color = constants.ORANGE_PASTEL
        self.label_text_render = constants.MY_FONT.render("collider", True, self.color, None)

    def update(self) -> None:
        self.__realign_with_game_object_owner(self.owner)

    def get_inner_rect_copy(self) -> Rect:
        return self.__inner_rect.copy()

    def is_there_overlap_with_point(self, point: pygame.Vector2) -> bool:
        return self.__inner_rect.collidepoint(point.x, point.y)

    def is_there_overlap_with_rect(self, rect: pygame.Rect) -> bool:
        return self.__inner_rect.colliderect(rect)

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
        pygame.draw.rect(game_surface, self.color, self.__inner_rect, constants.GIZMOS_WIDTH)
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

    def update(self) -> None:
        self.__has_key_been_fired_at_this_frame = False
        self.__has_key_been_released_at_this_frame = False
        if self.is_key_being_held_down and not self.__has_key_been_already_fired_but_not_released and not self.__has_key_been_fired_at_this_frame:
            self.__has_key_been_fired_at_this_frame = True
            self.total_times_fired += 1
            self.__has_key_been_already_fired_but_not_released = True
        if self.__has_key_been_already_fired_but_not_released and not self.is_key_being_held_down:
            self.__has_key_been_already_fired_but_not_released = False
            self.__has_key_been_released_at_this_frame = True


# ----------------------------------------------------------------------------------------------------------------------


class Timer(Component):

    # can execute a function oce the timer is over
    def __init__(self, duration_in_ms, func=None):
        super().__init__("Timer")
        self.__duration_in_ms = duration_in_ms
        self.__start_time = 0
        self.__curren_moment = 0
        self.__is_active = False
        self.func = func

    @property
    def is_timer_active(self):
        return self.__is_active

    @property
    def elapsed_time(self):
        return self.__curren_moment - self.__start_time

    def get_duration_in_ms(self):
        return self.__duration_in_ms

    def set_duration_in_ms(self, new_duration_in_ms):
        self.__duration_in_ms = new_duration_in_ms

    def activate(self):
        self.__is_active = True
        self.__start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.__is_active = False
        self.__start_time = 0

    def update(self):
        self.__curren_moment = pygame.time.get_ticks()
        # if it has finished counting
        if self.elapsed_time > self.__duration_in_ms and self.__is_active:
            self.deactivate()
            # if function is not none
            if self.func:
                self.func()
