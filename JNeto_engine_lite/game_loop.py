import sys
import pygame
from pygame import *
from JNeto_engine_lite import constants
from JNeto_engine_lite.components import KeyTracker
from JNeto_engine_lite.scene_and_game_objects import Scene


class GameLoop:

    RESOLUTION = (1280, 720)
    __current_scene: Scene = None
    Delta_Time = 0
    Horizontal_Axis = 0
    Vertical_Axis = 0

    def __init__(self):

        # inits pygame
        pygame.init()

        # screen

        self.game_surface = pygame.display.set_mode(GameLoop.RESOLUTION)

        # fps
        self.clock = pygame.time.Clock()

        # gizmos
        self.gismoz_activation_tracker = KeyTracker(pygame.K_z)
        self.show_gizmos = False

    def run(self, default_scene: Scene):

        self.set_current_scene(default_scene)

        while True:
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
            GameLoop.__update_axis()
            self.gismoz_activation_tracker.update(None)
            if self.gismoz_activation_tracker.has_key_been_fired_at_this_frame:
                self.show_gizmos = not self.show_gizmos

            # UPDATES
            pygame.display.set_caption(f"JNETO PRODUCTIONS LITE GAME ENGINE |  FPS {self.clock.get_fps():.1f}")
            GameLoop.Delta_Time = self.clock.tick() / 1000
            GameLoop.__current_scene.update()

            # RENDER
            self.game_surface.fill(constants.GREY)  # clears screen
            GameLoop.__current_scene.render()
            if self.show_gizmos:
                GameLoop.__current_scene.render_gizmos(self.game_surface)
            pygame.display.update()

    @staticmethod
    def set_current_scene(scene: Scene):
        GameLoop.__current_scene = scene

    @staticmethod
    def get_current_scene() -> Scene:
        return GameLoop.__current_scene

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
