import typing
import pygame
from pygame import Surface, Color
from JNeto_engine_lite.components import Transform, Component, Sprite


# =====================================================================================================================
# =====================================================================================================================


class GameObject:

    ComponentSubclassType = typing.TypeVar('ComponentSubclassType', bound=Component)

    def __init__(self, name):
        self.name = name
        self.scene = None
        self.components: list[Component] = []
        self.transform: Transform = self.add_component(Transform())

    def start(self):
        pass

    def update(self):
        pass

    def render(self, game_surface: Surface):
        if self.has_component("Sprite"):
            sprite_component: Sprite = self.get_component("Sprite")
            sprite_component.image_rect = sprite_component.image.get_rect(center=self.transform.get_position_copy())
            game_surface.blit(sprite_component.image, sprite_component.image_rect.topleft)

    def render_gizmos(self, game_surface: Surface):
        # transform
        pygame.draw.circle(game_surface, Color("black"), self.transform.get_position_copy(), 5)
        # sprite
        if self.has_component("Sprite"):
            pygame.draw.rect(game_surface, Color("red"), self.get_component("sprite").image_rect, 2)

    def add_component(self, component) -> ComponentSubclassType:
        self.components.append(component)
        return component

    def has_component(self, name) -> bool:
        for component in self.components:
            if component.name == name.capitalize():
                return True
        return False

    def get_component(self, name: str) -> ComponentSubclassType:
        for component in self.components:
            if component.name == name.capitalize():
                return component
        raise Exception(f"Component ({name}) not found")


# =====================================================================================================================
# =====================================================================================================================


class Scene:

    def __init__(self, game_surface: Surface):
        self.__game_objects: list[GameObject] = []
        self.__game_surface = game_surface

    def update(self):
        for game_object in self.__game_objects:
            for component in game_object.components:
                component.update()
            game_object.update()

    def render(self):
        for game_object in self.__game_objects:
            game_object.render(self.__game_surface)

    def render_gizmos(self, game_surface: Surface):
        for game_object in self.__game_objects:
            game_object.render_gizmos(game_surface)

    def add_game_object(self, game_object: GameObject):
        self.__game_objects.append(game_object)
        game_object.scene = self
        game_object.start()

    def remove_game_object(self, game_object: GameObject):
        if game_object in self.__game_objects:
            self.__game_objects.remove(game_object)

    def get_game_object(self, name: str):
        for game_object in self.__game_objects:
            if game_object.name == name:
                return game_object
        raise Exception(f"GameObject ({name}) not found")
