from JNeto_engine_lite.components import Sprite
from JNeto_engine_lite.scene_and_game_objects import GameObject


class ScoreManager(GameObject):
    def __init__(self):
        super().__init__("score_manager")

        self.sprite = self.add_component(Sprite(""))