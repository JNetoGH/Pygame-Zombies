import math
import numpy.linalg
from pygame import Vector2, Surface
from JNeto_engine_lite import constants
from JNeto_engine_lite.components import Sprite, Collider
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject


class Zombie(GameObject):

    def __init__(self, initial_postion: Vector2):
        super().__init__("player")

        # Sprite Component
        self.sprite: Sprite = self.add_component(Sprite("res/Zombie.png"))
        self.sprite.scale_image(0.5)

        # Collider Component
        self.collider: Collider = self.add_component(Collider(0, 0, 35, 35))

        # movement and related
        self.move_speed = 75
        self.angle_to_player = 20
        self.angular_velocity = 100
        self.direction_to_player = Vector2(0, 0)

        # initial position
        self.transform.move_position(initial_postion)

    def update(self):

        # DISTANCE TO PLAYER (used to get the direction to player)
        player_position: Vector2 = GameLoop.get_current_scene().get_game_object("player").transform.get_position_copy()
        zombie_position: Vector2 = self.transform.get_position_copy()
        distance_to_player: Vector2 = player_position - self.transform.get_position_copy()

        # DIRECTION TO PLAYER: normalizes the dir, avoiding div by 0 exeptions, ex: vector=(0, 0)
        self.direction_to_player: Vector2 = distance_to_player
        if numpy.linalg.norm(distance_to_player) > 0:
            self.direction_to_player = self.direction_to_player / numpy.linalg.norm(self.direction_to_player)

        # MOVEMENT
        new_position: Vector2 = zombie_position + self.direction_to_player * self.move_speed * GameLoop.Delta_Time
        self.transform.move_position(new_position)

        # ANGLE (used for rotation, atan2 is used to get the angle between two points)
        up_direction = Vector2(0, 0)
        dx = up_direction.x - self.direction_to_player.x
        dy = up_direction.y - self.direction_to_player.y
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        self.angle_to_player = math.degrees(rads) + 90

        # KEEPS THE ANGLE IN 0º <=> 360º RANGE (it works with a 7232º angle, but I prefer keeping it in this range)
        self.angle_to_player = 0 + (self.angle_to_player - 360) if self.angle_to_player > 360 else self.angle_to_player # 0 + what passed from 360
        self.angle_to_player = self.angle_to_player = 360 - (self.angle_to_player * -1) if self.angle_to_player < 0 else self.angle_to_player  # 360 - what passed from 0

        # ROTATION
        self.sprite.rotate_image(self.angle_to_player)

    def render_gizmos(self, game_surface: Surface):
        super().render_gizmos(game_surface)
        constants.draw_special_gizmos(game_surface, self.transform.get_position_copy(), self.direction_to_player, self.angle_to_player)

    def destroy(self):
        GameLoop.get_current_scene().remove_game_object(self)