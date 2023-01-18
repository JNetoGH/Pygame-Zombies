import numpy
from pygame import *
import math
from engine_JNeto_LITE import constants
from engine_JNeto_LITE.components import Sprite, Collider, KeyTracker
from engine_JNeto_LITE.game_loop import GameLoop
from engine_JNeto_LITE.scene_and_game_objects import GameObject
from game_objects.game_object_buttons import ButtonManager
from game_objects.game_object_map import Barrier
from game_objects.game_object_zombie_instantiator import ZombieInstantiator
from game_objects.game_object_projectiles import RotatableProjectile, Bullet


class Player(GameObject):

    def __init__(self, initial_position: Vector2):
        super().__init__("player")

        self.game_over = False

        # Sprite Component
        self.sprite: Sprite = self.add_component(Sprite("game_art/humanShootgun.png"))
        self.sprite.scale_image(0.4)

        # Collider Component
        self.collider: Collider = self.add_component(Collider(0, 0, 35, 35))
        self.collider.collidable_classes.append(Barrier)
        self.collider.collidable_classes.append(ZombieInstantiator)

        # Key Tracker Component (for shooting)
        self.space_tracker: KeyTracker = self.add_component(KeyTracker(K_SPACE))

        # movement and related
        self.move_speed = 175
        self.angle = 20
        self.angular_velocity = 150
        self.direction = Vector2()

        # initial position
        self.transform.move_position(initial_position)

    def update(self):

        if self.game_over:
            GameLoop.STOP = True

        # ANGLE INCREMENT (for direciton)
        if GameLoop.Horizontal_Axis == 1:
            self.angle = self.angle - self.angular_velocity * GameLoop.Delta_Time
        elif GameLoop.Horizontal_Axis == -1:
            self.angle = self.angle + self.angular_velocity * GameLoop.Delta_Time

        # KEEPS THE ANGLE IN 0º <=> 360º RANGE (in order to work with my cached texts for perfromance)
        self.angle = constants.get_converted_angle_to_0_360_range(self.angle)

        # ROTATION (towards angle)
        self.sprite.rotate_image(self.angle)

        # DIRECTION (from angle in radians)
        angle_as_radians = (self.angle + 90) * math.pi / 180  # +90º because the img faces ↑, so the default → turns ↑
        self.direction = Vector2(math.cos(angle_as_radians), - math.sin(angle_as_radians))
        # normalizes the dir, avoiding div by 0 exceptions, ex: vector=(0, 0)
        if numpy.linalg.norm(self.direction) > 0:
            self.direction = self.direction / numpy.linalg.norm(self.direction)

        # MOVEMENT
        is_moving: bool = GameLoop.Vertical_Axis == -1
        if is_moving:
            # moves linearny to the new position (frame-rate independentily)
            current_position = self.transform.get_position_copy()
            new_postion = current_position + self.direction * self.move_speed * GameLoop.Delta_Time
            self.transform.move_position(new_postion)

        # SHOOT (current weapon is controlled by buttons)
        if self.space_tracker.has_key_been_fired_at_this_frame:
            if ButtonManager.CurrentWeapon == 0:
                self.scene.add_game_objects(Bullet(self.transform.get_position_copy(), self.direction, self.angle))
            elif ButtonManager.CurrentWeapon == 1:
                self.scene.add_game_objects(RotatableProjectile(self))

    def render_gizmos(self, game_surface: Surface):
        constants.draw_special_gizmos(game_surface, self.transform.get_position_copy(), self.direction, self.angle)
