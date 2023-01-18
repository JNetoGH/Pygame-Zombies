import pygame

from engine_JNeto_LITE.components import Sprite, Collider
from engine_JNeto_LITE.scene_and_game_objects import GameObject
from pygame import Vector2


class ButtonManager(GameObject):

    CurrentWeapon = 0
    Buttons = []

    def __init__(self):
        super().__init__("button_manager")

    def start(self):

        button_gun = ProjectileButton(0, "game_art/buttons/gun_unselected.png",
                                      "game_art/buttons/gun_hover.png",
                                      "game_art/buttons/gun_selected.png",
                                      Vector2(800, 650), 0.75)

        button_shuriken = ProjectileButton(1, "game_art/buttons/shuriken_unselected.png",
                                           "game_art/buttons/shuriken_hover.png",
                                           "game_art/buttons/shuriken_selected.png",
                                           Vector2(950, 650), 0.75)

        button_gun.is_selected = True
        ButtonManager.Buttons.append(button_gun)
        ButtonManager.Buttons.append(button_shuriken)

        for button in ButtonManager.Buttons:
            self.scene.add_game_objects(button)


class ProjectileButton(GameObject):
    def __init__(self, weapon_number, path_unselected: str, path_hover: str, path_selected: str,
                 position: Vector2, scale):
        super().__init__("projectile_button")

        self.weapon_number = weapon_number
        self.button_click_sound = pygame.mixer.Sound("game_art/buttons/button_click.wav")

        # postion
        self.transform.move_position(position)

        # paths imgs and sprite
        self.path_unselected = path_unselected
        self.path_hover = path_hover
        self.path_selected = path_selected
        self.sprite: Sprite = self.add_component(Sprite(self.path_unselected))
        self.scale = scale
        self.sprite.scale_image(self.scale)

        self.is_selected = False
        self.collider = self.add_component(Collider(0, 0, self.sprite.image.get_width(), self.sprite.image.get_height()))

    def update(self) -> None:

        if self.is_selected:
            self.sprite.change_image(self.path_selected)
            self.sprite.scale_image(self.scale)

        elif self.collider.is_there_overlap_with_point(Vector2(pygame.mouse.get_pos())):
            self.sprite.change_image(self.path_hover)
            self.sprite.scale_image(self.scale)
            if pygame.mouse.get_pressed(3)[0]:
                self.button_click_sound.play()
                self.is_selected = True
                ButtonManager.CurrentWeapon = self.weapon_number
                for button in ButtonManager.Buttons:
                    if button is self:
                        continue
                    button.is_selected = False
        else:
            self.sprite.change_image(self.path_unselected)
            self.sprite.scale_image(self.scale)
