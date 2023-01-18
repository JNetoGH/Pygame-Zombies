import sys
import pygame
from pygame import *
from engine_JNeto_LITE.scene_and_game_objects import Scene
pygame.init()


class GameLoop:

    STOP: bool = False
    RESOLUTION = (1280, 720)
    GameSurface = pygame.display.set_mode(RESOLUTION)
    __CurrentScene: Scene = None
    Delta_Time = 0
    Horizontal_Axis = 0
    Vertical_Axis = 0

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.show_gizmos = False

    def run(self, default_scene: Scene):

        self.set_current_scene(default_scene)

        while True:

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == K_z:
                    self.show_gizmos = not self.show_gizmos
            GameLoop.__update_axis()

            if GameLoop.STOP:
                continue

            # UPDATES
            pygame.display.set_caption(f"JNETO PRODUCTIONS LITE GAME ENGINE |  FPS {self.clock.get_fps():.1f}")
            GameLoop.Delta_Time = self.clock.tick() / 1000
            GameLoop.__CurrentScene.update()

            # RENDER
            # self.GameSurface.fill(constants.GREY)  # clears screen
            GameLoop.__CurrentScene.render()
            if self.show_gizmos:
                GameLoop.__CurrentScene.render_gizmos(self.GameSurface)
            pygame.display.update()

            # DEBUGGIN
            # print(f"Total Game Objects in scene: {len(self.__CurrentScene.game_objects)}\n")

    @staticmethod
    def set_current_scene(scene: Scene):
        GameLoop.__CurrentScene = scene

    @staticmethod
    def get_current_scene() -> Scene:
        return GameLoop.__CurrentScene

    @staticmethod
    def __update_axis():
        keys = pygame.key.get_pressed()
        GameLoop.Horizontal_Axis, GameLoop.Vertical_Axis = 0, 0
        # vertical axis
        if keys[K_w] or keys[K_UP]:
            GameLoop.Vertical_Axis = -1
        elif keys[K_s] or keys[K_DOWN]:
            GameLoop.Vertical_Axis = 1
        # horizontal axis
        if keys[K_a] or keys[K_LEFT]:
            GameLoop.Horizontal_Axis = -1
        elif keys[K_d] or keys[K_RIGHT]:
            GameLoop.Horizontal_Axis = 1
