from engine_JNeto_LITE import constants
from engine_JNeto_LITE.components import Sprite
from engine_JNeto_LITE.game_loop import GameLoop
from engine_JNeto_LITE.scene_and_game_objects import GameObject
from pygame import Vector2, Surface, font


class ScoreManager(GameObject):

    Score = 0
    ScoreFont = font.Font(constants.FONT_PATH, 22)
    ScoreText = ScoreFont.render(f"{Score}", True, constants.WHITE)

    def __init__(self):
        super().__init__("score_manager")

        # sprite
        self.sprite = self.add_component(Sprite("game_art/log_ui.png"))
        self.transform.move_position(Vector2(GameLoop.RESOLUTION[0] / 4, 40))

        # score text
        self.score_text_position = (GameLoop.RESOLUTION[0] // 4+10, 24)

    def render(self, game_surface: Surface):
        super().render(game_surface)
        game_surface.blit(ScoreManager.ScoreText, self.score_text_position)