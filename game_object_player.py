import numpy
from pygame import *
import math
from JNeto_engine_lite import constants
from JNeto_engine_lite.components import Sprite, Collider, KeyTracker
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject
from game_object_barrier import Barrier
from game_object_bullet import Bullet
from game_object_zombie_instantiator import ZombieInstantiator


class Player(GameObject):

    def __init__(self, initial_position: Vector2):
        super().__init__("player")

        # Sprite Component
        self.sprite: Sprite = self.add_component(Sprite("res/HumanShootgun.png"))
        self.sprite.scale_image(0.4)

        # Collider Component
        self.collider: Collider = self.add_component(Collider(0, 0, 35, 35))
        self.collider.collidable_classes.append(Barrier)
        self.collider.collidable_classes.append(ZombieInstantiator)

        # Key Tracker Component (for shooting)
        self.space_tracker = self.add_component(KeyTracker(K_SPACE))

        # movement and related
        self.move_speed = 200
        self.angle = 20
        self.angular_velocity = 150
        self.direction = Vector2()

        # initial position
        self.transform.move_position(initial_position)

    def update(self):

        # ANGLE INCREMENT (for direciton)
        if GameLoop.Horizontal_Axis == 1:
            self.angle = self.angle - self.angular_velocity * GameLoop.Delta_Time
        elif GameLoop.Horizontal_Axis == -1:
            self.angle = self.angle + self.angular_velocity * GameLoop.Delta_Time

        # KEEPS THE ANGLE IN 0º <=> 360º RANGE (it works with a 7232º angle, but I prefer keeping it in this range)
        self.angle = self.angle = 0 + (self.angle - 360) if self.angle > 360 else self.angle  # 0 + what passed from 360
        self.angle = self.angle = 360 - (self.angle * -1) if self.angle < 0 else self.angle   # 360 - what passed from 0

        # ROTATION (towards angle)
        self.sprite.rotate_image(self.angle)

        # DIRECTION (from angle in radians)
        angle_as_radians = (self.angle + 90) * math.pi / 180  # +90º because the img faces ↑, so the default → turns ↑
        self.direction = Vector2(math.cos(angle_as_radians), - math.sin(angle_as_radians))
        if numpy.linalg.norm(self.direction) > 0:  # normalizes the dir, avoiding div by 0 exeptions, ex: vector=(0, 0)
            self.direction = self.direction / numpy.linalg.norm(self.direction)

        # MOVEMENT
        is_moving: bool = GameLoop.Vertical_Axis == -1
        if is_moving:
            # moves linearny to the new position (frame-rate independentily)
            current_position = self.transform.get_position_copy()
            new_postion = current_position + self.direction * self.move_speed * GameLoop.Delta_Time
            self.transform.move_position(new_postion)

        # SHOOT
        if self.space_tracker.has_key_been_fired_at_this_frame:
            self.scene.add_game_objects(Bullet(self.transform.get_position_copy(), self.direction, self.angle))

    def render_gizmos(self, game_surface: Surface):
        constants.draw_special_gizmos(game_surface, self.transform.get_position_copy(), self.direction, self.angle)
