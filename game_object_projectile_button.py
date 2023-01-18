import pygame

from engine_JNeto_LITE.components import Sprite, Collider
from engine_JNeto_LITE.scene_and_game_objects import GameObject
from pygame import Vector2


class ProjectileButton(GameObject):
    def __init__(self, path_normal: str, path_hoover: str, path_active: str, position: Vector2, scale, func):
        super().__init__("projectile_button")

        self.button_click_sound = pygame.mixer.Sound("game_sounds/button_click.wav")

        # postion
        self.transform.move_position(position)

        # paths imgs
        self.path_normal = path_normal
        self.path_hoover = path_hoover
        self.path_active = path_active

        # sprite
        self.sprite = self.add_component(Sprite(self.path_normal))
        self.scale = scale
        self.sprite.scale_sprite(scale)

        self.collider = self.add_component(Collider(0, 0, self.sprite.image.get_width(), self.sprite.get_height()))
        self.func = func

    def game_object_update(self) -> None:

        if self.collider.is_there_overlap_with_point(Vector2(pygame.mouse.get_pos())):
            self.sprite.change_image(self.path_active)
            self.sprite.scale_sprite(self.scale)
            if pygame.mouse.get_pressed(3)[0]:
                self.button_click_sound.play()
                self.func()
        else:
            self.sprite.change_image(self.path_normal)
            self.sprite.scale_sprite(self.scale)
