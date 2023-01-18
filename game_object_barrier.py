from JNeto_engine_lite.components import Collider
from JNeto_engine_lite.scene_and_game_objects import GameObject
from pygame import Vector2


class Barrier(GameObject):

    def __init__(self, position: Vector2):
        super().__init__("barrier")

        # Collider Component
        self.collider: Collider = self.add_component(Collider(0, 0, 250, 30))

        # POSITION
        self.transform.move_position(position)
