from pygame import Surface
from JNeto_engine_lite.components import Sprite, Vector2
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject


class Bullet(GameObject):

    def __init__(self, player_position, player_direction, angle):
        super().__init__("bullet")

        # SPRITE
        self.sprite: Sprite = self.add_component(Sprite("res/bullet.png"))
        self.sprite.scale_image(0.75)
        self.sprite.rotate_image(angle)

        # MOVEMENT
        self.speed = 300
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

        # DESCTRUCTION FOR GARBAGE COLLECTION
        pos = self.transform.get_position_copy()
        out_of_screen = not (0 < pos.x < GameLoop.RESOLUTION[0] and 0 < pos.y < GameLoop.RESOLUTION[1])
        if out_of_screen:
            self.destroy()

    def destroy(self):
        GameLoop.get_current_scene().remove_game_object(self)

    def render_gizmos(self, game_surface: Surface):
        pass
