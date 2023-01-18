import math
import numpy.linalg
from pygame import Vector2, Surface
from engine_JNeto_LITE import constants
from engine_JNeto_LITE.components import Sprite, Collider
from engine_JNeto_LITE.game_loop import GameLoop
from engine_JNeto_LITE.scene_and_game_objects import GameObject
from game_objects.game_object_map import Barrier


class Zombie(GameObject):

    def __init__(self, initial_postion: Vector2):
        super().__init__("zombie")

        self.player = None

        # Sprite Component
        self.sprite: Sprite = self.add_component(Sprite("game_art/zombie.png"))
        self.sprite.scale_image(0.4)

        # Collider Component
        self.collider: Collider = self.add_component(Collider(0, 0, 35, 35))
        self.collider.collidable_classes.append(Barrier)

        # movement and related
        self.move_speed = 75
        self.angle_to_player = 20
        self.angular_velocity = 80
        self.direction_to_player = Vector2(0, 0)

        # initial position
        self.transform.move_position(initial_postion)

    def start(self):
        self.player = self.scene.get_game_object("player")

    def update(self):

        # DISTANCE TO PLAYER (used to get the direction to player)
        player_position = self.player.transform.get_position_copy()
        zombie_position = self.transform.get_position_copy()
        distance_to_player = player_position - self.transform.get_position_copy()

        # DIRECTION TO PLAYER (normalizes the dir, avoiding div by 0 exeptions, ex: vector=(0, 0))
        self.direction_to_player = distance_to_player
        if numpy.linalg.norm(distance_to_player) > 0:
            self.direction_to_player = self.direction_to_player / numpy.linalg.norm(self.direction_to_player)

        # MOVEMENT (do not transpass barries)
        new_position = zombie_position + self.direction_to_player * self.move_speed * GameLoop.Delta_Time
        self.transform.move_position(new_position)

        # ANGLE (used for rotation, atan2 is used to get the angle between two points)
        up_direction = Vector2(0, 0)
        dx = up_direction.x - self.direction_to_player.x
        dy = up_direction.y - self.direction_to_player.y
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        # converts radians to degrees
        self.angle_to_player = (rads * 180/math.pi) + 90  # +90º because the img faces ↑, so the default → turns ↑

        # KEEPS THE ANGLE IN 0º <=> 360º RANGE (in order to work with my cached texts for perfromance)
        self.angle_to_player = constants.get_converted_angle_to_0_360_range(self.angle_to_player)

        # ROTATION
        self.sprite.rotate_image(self.angle_to_player)

        # COLLISION WITH PLAYER
        if self.collider.is_there_overlap_with_rect(self.player.collider.get_inner_rect_copy()):
            self.scene.add_game_objects(GameOverImage())
            self.player.game_over = True

    def render_gizmos(self, game_surface: Surface):
        # distance to player
        constants.draw_special_gizmos(game_surface, self.transform.get_position_copy(), self.direction_to_player, self.angle_to_player)

    def destroy(self):
        self.scene.remove_game_object(self)


class GameOverImage(GameObject):
    def __init__(self):
        super().__init__("game_over_img")
        self.sprite: Sprite = self.add_component(Sprite("game_art/game_over.png"))
        self.sprite.scale_image(2)
        self.transform.move_position(Vector2(GameLoop.RESOLUTION[0]//2, GameLoop.RESOLUTION[1]//2))