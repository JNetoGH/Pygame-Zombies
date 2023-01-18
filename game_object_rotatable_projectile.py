from JNeto_engine_lite.components import Sprite, Collider
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject
from game_object_zombie import Zombie
from pygame import Vector2
import math


class RotatableProjectile(GameObject):

    def __init__(self, player: GameObject):
        super().__init__("rotatable")

        # sprite
        self.sprite: Sprite = self.add_component(Sprite("res/shuriken_project.png"))
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
                    game_object.destroy()
                    self.destroy()

        # SPRITE SPINNING ANIMATION
        self.sprite.rotate_image(self.sprite_spinning_angle)
        self.sprite_spinning_angle += self.sprite_spinnin_velocity * GameLoop.Delta_Time

    def destroy(self):
        self.scene.remove_game_object(self)
