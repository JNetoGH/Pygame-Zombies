import pygame.image
from pygame import *
import math
from JNeto_engine_lite.components import Sprite
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject


class Player(GameObject):

    Horizontal_Axis = 0
    Vertical_Axis = 0

    def __init__(self):
        super().__init__("player")

    def start(self):
        self.add_component(Sprite("res/characters/Human.png"))
        self.sprite_component: Sprite = self.get_component("Sprite")
        self.sprite_component.scale_image(0.5)
        self.buffered_original_image = self.sprite_component.image
        self.move_speed = 200
        self.angle = 0
        self.angular_velocity = 100

    def update(self):

        # inputs
        Player.treat_axis()

        # angle
        print(f"angle: {self.angle}")
        if Player.Horizontal_Axis == 1:
            self.angle = self.angle - self.angular_velocity * GameLoop.Delta_Time
        elif Player.Horizontal_Axis == -1:
            self.angle = self.angle + self.angular_velocity * GameLoop.Delta_Time

        # rotate
        self.sprite_component.image = pygame.transform.rotate(self.buffered_original_image, self.angle)

        # direction
        angle_as_radians = math.radians(self.angle + 90)
        dir = Vector2(math.cos(angle_as_radians), - math.sin(angle_as_radians))
        dir = dir if dir.magnitude() == 0 else dir.normalize()

        # movement
        if Player.Vertical_Axis == -1:
            self.transform.position = self.transform.position + dir * self.move_speed * GameLoop.Delta_Time

    @staticmethod
    def treat_axis():
        keys = pygame.key.get_pressed()
        Player.Horizontal_Axis, Player.Vertical_Axis = 0, 0

        # vertical axis
        if keys[K_w] or keys[K_UP]:
            Player.Vertical_Axis = -1
        elif keys[K_s] or keys[K_DOWN]:
            Player.Vertical_Axis = 1

        # horizontal axis
        if keys[K_a] or keys[K_LEFT]:
            Player.Horizontal_Axis = -1
        elif keys[K_d] or keys[K_RIGHT]:
            Player.Horizontal_Axis = 1
