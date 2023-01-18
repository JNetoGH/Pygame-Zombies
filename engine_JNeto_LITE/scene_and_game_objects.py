import typing

import pygame.mouse
from pygame import Surface

from engine_JNeto_LITE import constants
from engine_JNeto_LITE.components import Transform, Component, Sprite, Collider


# =====================================================================================================================
# =====================================================================================================================


class GameObject:

    ComponentSubclassType = typing.TypeVar('ComponentSubclassType', bound=Component)

    def __init__(self, name):
        self.name = name

        # rendering cache for performance
        self.has_sprite_component = False
        self.sprite_component = None

        # colision cache for performance
        self.has_collider_component = False
        self.collider_component = None

        self.scene = None
        self.components: list[Component] = []
        self.transform: Transform = self.add_component(Transform())
        self.cached_owner_name_gizmos_text = constants.MY_FONT.render(name, True, constants.WHITE, None)

    def start(self):
        pass

    def update(self):
        pass

    def render(self, game_surface: Surface):
        if self.has_sprite_component:
            self.sprite_component .image_rect = self.sprite_component .image.get_rect(center=self.transform.get_position_copy())
            game_surface.blit(self.sprite_component .image, self.sprite_component .image_rect.topleft)

    def render_gizmos(self, game_surface: Surface):
        pass

    def add_component(self, component) -> ComponentSubclassType:
        component.owner = self
        self.components.append(component)

        # sync for renderenring cache
        if not self.has_sprite_component and isinstance(component, Sprite):
            self.sprite_component = component
            self.has_sprite_component = True
        # sync for collision cache
        if not self.has_collider_component and isinstance(component, Collider):
            self.collider_component = component
            self.has_collider_component = True

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
        self.game_objects: list[GameObject] = []
        self.game_surface = game_surface

    def update(self):
        for game_object in self.game_objects:
            for component in game_object.components:
                component.update()
            game_object.update()

    def render(self):
        for game_object in self.game_objects:
            game_object.render(self.game_surface)

    def render_gizmos(self, game_surface: Surface):
        for game_object in self.game_objects:
            # GameObjects gizmos
            game_object.render_gizmos(game_surface)
            # Compenents gizmos
            for component in game_object.components:
                component.render_gizmos(game_surface)
            # Name gizmos
            name_pos = game_object.transform.get_position_copy()
            name_pos.x += 5
            name_pos.y = name_pos.y - game_object.cached_owner_name_gizmos_text.get_height()/2
            game_surface.blit(game_object.cached_owner_name_gizmos_text, name_pos)

        # Mouse Gizmos
        mouse_render = constants.MY_FONT.render(f"mouse: {pygame.mouse.get_pos()}", True, constants.CYAN_PASTEL, None)
        game_surface.blit(mouse_render, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 20))

    def add_game_objects(self, *game_objects: GameObject):
        for gm_obj in game_objects:
            self.game_objects.append(gm_obj)
            gm_obj.scene = self
            gm_obj.start()

    def remove_game_object(self, game_object: GameObject):
        if game_object in self.game_objects:
            self.game_objects.remove(game_object)

    def get_game_object(self, name: str):
        for game_object in self.game_objects:
            if game_object.name == name:
                return game_object
        raise Exception(f"GameObject ({name}) not found")
