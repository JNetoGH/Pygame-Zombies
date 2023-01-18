import pygame
from pygame import Vector2
from engine_JNeto_LITE.components import Timer, Collider
from engine_JNeto_LITE.scene_and_game_objects import GameObject
from game_objects.game_object_zombie import Zombie
import random


class ZombieInstantiator(GameObject):

    def __init__(self, position: Vector2, width, height, instantiation_frequency_in_seg):
        super().__init__("zombie instantiator")
        self.position = position
        self.transform.move_position(position)
        self.instantiation_frequency_in_seg = instantiation_frequency_in_seg

        self.instantiated_zombies = 0
        self.timer: Timer = self.add_component(Timer(self.instantiation_frequency_in_seg * 1000, self.instantiate_zombie))
        self.instantiation_area: Collider = self.add_component(Collider(0, 0, width, height))

    def update(self):
        if not self.timer.is_timer_active:
            self.timer.activate()
            # pregressive difficulty
            self.instantiation_frequency_in_seg -= 0.1
            self.instantiation_frequency_in_seg = 0.25 if self.instantiation_frequency_in_seg < 0.25 else self.instantiation_frequency_in_seg
            self.timer.set_duration_in_ms(self.instantiation_frequency_in_seg * 1000)

    def instantiate_zombie(self):
        # sets a random point inside the instantiation rect
        instantiation_rect = self.instantiation_area.get_inner_rect_copy()
        start_range_point_x = self.position.x - instantiation_rect.width / 2
        end_range_point_x = self.position.x + instantiation_rect.width / 2
        start_range_point_y = self.position.y - instantiation_rect.height / 2
        end_range_point_y = self.position.y + instantiation_rect.height / 2

        zombie_position = Vector2(0,0)
        zombie_position.x = random.randint(round(start_range_point_x), round(end_range_point_x))
        zombie_position.y = random.randint(round(start_range_point_y), round(end_range_point_y))

        self.scene.add_game_objects(Zombie(pygame.Vector2(zombie_position)))