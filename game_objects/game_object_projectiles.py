import pygame
from pygame import Surface, Vector2
from engine_JNeto_LITE import constants
from engine_JNeto_LITE.components import Sprite, Collider
from engine_JNeto_LITE.game_loop import GameLoop
from engine_JNeto_LITE.scene_and_game_objects import GameObject
from game_objects.game_object_score_manager import ScoreManager
from game_objects.game_object_zombie import Zombie
import math


# =====================================================================================================================
# =====================================================================================================================


class Bullet(GameObject):

    def __init__(self, player_position, player_direction, angle):
        super().__init__("bullet")

        # Sprite Component
        self.sprite: Sprite = self.add_component(Sprite("game_art/bullet.png"))
        self.sprite.scale_image(0.75)
        self.angle = angle
        self.sprite.rotate_image(self.angle)

        # Collider Component
        self.collider: Collider = self.add_component(Collider(0, 0, 10, 10))

        # MOVEMENT
        self.speed = 350
        self.direction = player_direction
        self.INSTANCIATION_DISTANCE = 35
        self.initial_position = player_position + self.direction * self.INSTANCIATION_DISTANCE

        # INITIAL POSITION
        self.transform.move_position(self.initial_position)

    def start(self):
        pygame.mixer.Sound("game_art/shot.wav").play()

    def update(self):

        # MOVES THE BULLET LINEARLY
        current_position = self.transform.get_position_copy()
        new_position = current_position + self.direction * self.speed * GameLoop.Delta_Time
        self.transform.move_position(new_position)

        # SETS FOR GARBAGE COLLECTION WHEN EXITS THE SCREEN
        pos = self.transform.get_position_copy()
        out_of_screen = not (0 < pos.x < GameLoop.RESOLUTION[0] and 0 < pos.y < GameLoop.RESOLUTION[1])
        if out_of_screen:
            self.destroy()

        # COLLISION WITH ZOMBIE (destorys bullet and zombie)
        for game_object in self.scene.game_objects:
            if isinstance(game_object, Zombie):
                if self.collider.is_there_overlap_with_rect(game_object.collider.get_inner_rect_copy()):
                    ScoreManager.Score += 1
                    ScoreManager.ScoreText = ScoreManager.ScoreFont.render(f"{ScoreManager.Score}", True, constants.WHITE)
                    game_object.destroy()
                    self.destroy()

    def render_gizmos(self, game_surface: Surface):
        constants.draw_special_gizmos(game_surface, self.transform.get_position_copy(), self.direction, self.angle)

    def destroy(self):
        self.scene.remove_game_object(self)


# =====================================================================================================================
# =====================================================================================================================


class RotatableProjectile(GameObject):

    def __init__(self, player: GameObject):
        super().__init__("rotatable")

        # sprite
        self.sprite: Sprite = self.add_component(Sprite("game_art/shuriken_project.png"))
        self.sprite.scale_image(1)
        self.sprite_spinning_angle = 0
        self.sprite_spinnin_velocity = 250

        # collider
        self.collider: Collider = self.add_component(Collider(0, 0, 30, 30))

        # ROTATION
        self.player = player
        self.angle = 0
        self.angular_velocity = 4
        self.DISTANCE_FROM_ORIGIN = 80

    def start(self):
        pygame.mixer.Sound("game_art/slash.wav").play()

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

        # COLLISION WITH ZOMBIE (destorys bullet and zombie)
        for game_object in self.scene.game_objects:
            if isinstance(game_object, Zombie):
                if self.collider.is_there_overlap_with_rect(game_object.collider.get_inner_rect_copy()):
                    pygame.mixer.Sound("game_art/star.wav").play()
                    ScoreManager.Score += 1
                    ScoreManager.ScoreText = ScoreManager.ScoreFont.render(f"{ScoreManager.Score}", True, constants.WHITE)
                    game_object.destroy()
                    self.destroy()

        # SPRITE SPINNING ANIMATION
        self.sprite.rotate_image(self.sprite_spinning_angle)
        self.sprite_spinning_angle += self.sprite_spinnin_velocity * GameLoop.Delta_Time

    def destroy(self):
        self.scene.remove_game_object(self)


# =====================================================================================================================
# =====================================================================================================================

# class Boomorang()