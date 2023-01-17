import pygame.image
import numpy
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

        # gizmos caching (texs intantiations are to have in pygame, so i am caching them all)
        self.LINE_SIZES = 100
        self.FONT_SIZE = 20
        self.font = pygame.font.Font("JNeto_engine_lite/engine_res/JetBrainsMono-Medium.ttf", self.FONT_SIZE)
        self.cached_text_reder_origin = self.font.render("0º", True, Color("yellow"), None)
        self.cached_angles = [self.font.render(f"dir: {i}º", True, Color("white"), None) for i in range(0, 361)]

        # sprite
        self.sprite_component: Sprite = self.add_component(Sprite("res/characters/Human.png"))
        self.sprite_component.scale_image(0.5)
        self.buffered_original_image = self.sprite_component.image

        # movement and related
        self.move_speed = 200
        self.angle = 20
        self.angular_velocity = 100
        self.direction = Vector2()

    def start(self):
        # initial position
        self.transform.set_position(Vector2(200, 200))

    def update(self):
        # INPUTS
        Player.update_axis()

        # ANGLE INCREMENT (for direciton)
        if Player.Horizontal_Axis == 1:
            self.angle = self.angle - self.angular_velocity * GameLoop.Delta_Time
        elif Player.Horizontal_Axis == -1:
            self.angle = self.angle + self.angular_velocity * GameLoop.Delta_Time

        # KEEPS THE ANGLE IN 0º <=> 360º RANGE (it works with a 7232º angle, but I prefer keeping it in this range)
        self.angle = self.angle = 0 + (self.angle - 360) if self.angle > 360 else self.angle  # 0 + what passed from 360
        self.angle = self.angle = 360 - (self.angle * -1) if self.angle < 0 else self.angle   # 360 - what passed from 0

        # ROTATION (towards angle)
        self.sprite_component.image = pygame.transform.rotate(self.buffered_original_image, self.angle)

        # DIRECTION (from angle in radians)
        angle_as_radians = (self.angle + 90) * math.pi / 180  # +90º because the img faces ↑, so the default → turns ↑
        self.direction = Vector2(math.cos(angle_as_radians), - math.sin(angle_as_radians))
        if numpy.linalg.norm(self.direction) > 0:  # normalizes the dir, avoiding div by 0 exeptions, ex: vector=(0, 0)
            self.direction = self.direction / numpy.linalg.norm(self.direction)

        # MOVEMENT
        is_moving: bool = Player.Vertical_Axis == -1
        if is_moving:
            # moves linearny to the new position (frame-rate independentily)
            current_position = self.transform.get_position_copy()
            new_postion = current_position + self.direction * self.move_speed * GameLoop.Delta_Time
            self.transform.set_position(new_postion)

    def render_gizmos(self, game_surface: Surface):
        super().render_gizmos(game_surface)

        # player 0ª line
        start = self.transform.get_position_copy()
        end = self.transform.get_position_copy() + Vector2(0, -1) * self.LINE_SIZES
        pygame.draw.line(game_surface, Color("yellow"), start, end)
        end.x += 5
        game_surface.blit(self.cached_text_reder_origin, end)

        # player's direction
        end_player_dir = self.transform.get_position_copy() + self.direction * self.LINE_SIZES
        pygame.draw.line(game_surface, Color("white"), start, end_player_dir)
        game_surface.blit(self.cached_angles[int(self.angle)], end_player_dir)

        # player position to mouse position line
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(game_surface, Color("cyan"), start, mouse_pos)

    @staticmethod
    def update_axis():
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
