from JNeto_engine_lite import constants
from JNeto_engine_lite.components import Sprite
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject
from pygame import Vector2, Surface
import math


class RotatableProjectile(GameObject):

    def __init__(self):
        super().__init__("rotatable")

        # sprite
        sprite: Sprite = self.add_component(Sprite("res/shuriken.png"))

        # ROTATION
        self.player = None
        self.angle = 0
        self.angular_velocity = 5
        self.DISTANCE_FROM_ORIGIN = 80

    def start(self):
        self.player: GameObject = self.scene.get_game_object("player")

    def update(self):
        # INCREASES THE AGLE USING THE ANGLUAR VELOCITY (framerate independent, used in the rotation bellow)
        self.angle += self.angular_velocity * GameLoop.Delta_Time

        # ROTATING AROUND THE ORIGIN (0,0) USING ROTATION MATRIX OPERATION
        # clockwise equation:
        #    x` = x * cos(θ) - y * sin(θ)
        #    y` = x * sin(θ) + y * cos(θ)
        current_position = Vector2(self.DISTANCE_FROM_ORIGIN, self.DISTANCE_FROM_ORIGIN)
        new_position = Vector2(0, 0)
        new_position.x = current_position.x * math.cos(self.angle) - current_position.y * math.sin(self.angle)
        new_position.y = current_position.x * math.sin(self.angle) + current_position.y * math.cos(self.angle)

        # MOVES THE ROTATE ITEM BACK TO PLAYER
        self.transform.move_position(self.player.transform.get_position_copy() + new_position)



