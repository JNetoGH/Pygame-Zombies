import sys
import pygame
from pygame import *

from JNeto_engine_lite.scene_and_game_objects import Scene


class GameLoop:

    Delta_Time = 0

    def __init__(self):

        # inits pygame
        pygame.init()

        # screen
        resolution = (1280, 720)
        self.game_surface = pygame.display.set_mode(resolution)

        # fps
        self.clock = pygame.time.Clock()

        # scenes
        self.current_scene: Scene = None

    def run(self, default_scene: Scene):

        self.set_current_scene(default_scene)

        while True:
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()

            # UPDATES
            pygame.display.set_caption(f"JNETO PRODUCTIONS LITE GAME ENGINE |  FPS {self.clock.get_fps():.1f}")
            GameLoop.Delta_Time = self.clock.tick() / 1000
            self.current_scene.update()

            # RENDER
            # clears screen
            self.game_surface.fill(Color("blue"))
            self.current_scene.render()
            self.current_scene.render_gizmos(self.game_surface)
            pygame.display.update()

    def set_current_scene(self, scene: Scene):
        self.current_scene = scene
