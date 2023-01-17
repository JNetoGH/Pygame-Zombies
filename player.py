import pygame.image
import numpy
from pygame import *
import math
from JNeto_engine_lite import constants
from JNeto_engine_lite.components import Sprite, Collider, KeyTracker
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject
from bullet import Bullet


class Player(GameObject):

    def __init__(self):
        super().__init__("player")

        # gizmos caching (texs intantiations are to have in pygame, so i am caching them all)
        self.LINE_SIZES = 100
        self.LINE_WIDTHS = 2
        self.cached_origin_angle = constants.MY_FONT.render("0º", True, constants.YELLOW_PASTEL, None)
        self.cached_angles = [constants.MY_FONT.render(f"dir: {i}º", True, constants.PINK_PASTEL, None) for i in range(0, 361)]

        # Sprite Component
        self.sprite: Sprite = self.add_component(Sprite("res/HumanShootgun.png"))
        self.sprite.scale_image(0.5)

        # Collider Component
        self.collider: Collider = self.add_component(Collider(0, 18, 35, 22))

        # Key Tracker Component (for shooting)
        self.space_tracker = self.add_component(KeyTracker(K_SPACE))

        # movement and related
        self.move_speed = 200
        self.angle = 20
        self.angular_velocity = 100
        self.direction = Vector2()

    def start(self):
        # initial position
        self.transform.move_position(Vector2(200, 200))

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
            scene = GameLoop.get_current_scene()
            scene.add_game_objects(Bullet(self.transform.get_position_copy(), self.direction, self.angle))

    def render_gizmos(self, game_surface: Surface):
        super().render_gizmos(game_surface)

        # player 0ª line
        start = self.transform.get_position_copy()
        end = self.transform.get_position_copy() + Vector2(0, -1) * self.LINE_SIZES
        pygame.draw.line(game_surface, constants.YELLOW_PASTEL, start, end, self.LINE_WIDTHS)
        end.x += 5
        game_surface.blit(self.cached_origin_angle, end)

        # player's direction
        end_player_dir = self.transform.get_position_copy() + self.direction * self.LINE_SIZES
        pygame.draw.line(game_surface, constants.PINK_PASTEL, start, end_player_dir, self.LINE_WIDTHS)
        game_surface.blit(self.cached_angles[int(self.angle)], end_player_dir)

        # player position to mouse position line
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(game_surface, constants.CYAN_PASTEL, start, mouse_pos, self.LINE_WIDTHS)
