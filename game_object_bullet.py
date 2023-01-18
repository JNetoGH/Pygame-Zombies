from pygame import Surface
from JNeto_engine_lite import constants
from JNeto_engine_lite.components import Sprite, Collider
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject
from game_object_zombie import Zombie


class Bullet(GameObject):

    def __init__(self, player_position, player_direction, angle):
        super().__init__("bullet")

        # Sprite Component
        self.sprite: Sprite = self.add_component(Sprite("res/bullet.png"))
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
                    game_object.destroy()
                    self.destroy()

    def render_gizmos(self, game_surface: Surface):
        constants.draw_special_gizmos(game_surface, self.transform.get_position_copy(), self.direction, self.angle)

    def destroy(self):
        self.scene.remove_game_object(self)
