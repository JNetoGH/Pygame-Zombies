from engine_JNeto_LITE.components import Sprite, Collider
from engine_JNeto_LITE.game_loop import GameLoop
from engine_JNeto_LITE.scene_and_game_objects import GameObject
from pygame import Vector2


class Map(GameObject):
    def __init__(self, path_to_image: str):
        super().__init__("map")
        # position
        resolution = GameLoop.RESOLUTION
        self.transform.move_position(Vector2(resolution[0]//2, resolution[1]//2))
        # sprite
        self.sprite = self.add_component(Sprite(path_to_image))


# --------------------------------------------------------------------


class MapGrass(Map):
    def __init__(self):
        super().__init__("game_art/map.png")

    def start(self):

        rock_1 = Barrier(position=Vector2(593, 430), width=25, height=25)
        rock_2 = Barrier(position=Vector2(885, 405), width=25, height=25)
        stump_1 = Barrier(position=Vector2(880, 270), width=25, height=25)
        stump_2 = Barrier(position=Vector2(305, 525), width=25, height=25)
        wall_1 = Barrier(position=Vector2(130, 680), width=260, height=25)
        wall_2 = Barrier(position=Vector2(355, 650), width=200, height=25)
        wall_3 = Barrier(position=Vector2(550, 615), width=200, height=25)
        wall_4 = Barrier(position=Vector2(650, 568), width=140, height=50)
        wall_5 = Barrier(position=Vector2(775, 525), width=150, height=25)
        wall_6 = Barrier(position=Vector2(785, 500), width=25, height=25)
        wall_7 = Barrier(position=Vector2(810, 455), width=25, height=70)
        wall_8 = Barrier(position=Vector2(860, 425), width=70, height=25)
        wall_9 = Barrier(position=Vector2(907, 397), width=25, height=70)
        wall_10 = Barrier(position=Vector2(977, 365), width=100, height=25)
        wall_11 = Barrier(position=Vector2(1040, 340), width=25, height=70)
        wall_12 = Barrier(position=Vector2(1090, 300), width=70, height=25)
        wall_13 = Barrier(position=Vector2(1130, 255), width=25, height=70)
        wall_14 = Barrier(position=Vector2(1170, 115), width=25, height=200)
        wall_15 = Barrier(position=Vector2(790, 13), width=50, height=25)
        wall_16 = Barrier(position=Vector2(732, 47), width=50, height=25)
        wall_17 = Barrier(position=Vector2(665, 117), width=25, height=75)
        wall_18 = Barrier(position=Vector2(623, 155), width=75, height=25)
        wall_19 = Barrier(position=Vector2(535, 205), width=100, height=25)
        wall_20 = Barrier(position=Vector2(425, 240), width=75, height=25)
        wall_21 = Barrier(position=Vector2(270, 275), width=205, height=25)
        wall_22 = Barrier(position=Vector2(95, 315), width=100, height=25)
        wall_23 = Barrier(position=Vector2(32, 365), width=25, height=75)

        self.scene.add_game_objects(rock_1, rock_2, stump_1, stump_2,
            wall_1, wall_2, wall_3, wall_4, wall_5, wall_6, wall_7, wall_8, wall_9,wall_10, wall_11, wall_12, wall_13, wall_14,
            wall_15, wall_16, wall_17, wall_18, wall_19, wall_20, wall_21, wall_22, wall_23)



#--------------------------------------------------------------------


class MapCave(Map):
    def __init__(self):
        super().__init__("game_art/map.png")

    def start(self):
        example_barrier = Barrier(position=Vector2(10, 500), width=30, height=30)
        example_barrier2 = Barrier(position=Vector2(40, 500), width=10, height=100)
        self.scene.add_game_objects(example_barrier, example_barrier2)


class Barrier(GameObject):

    def __init__(self, position: Vector2, width, height):
        super().__init__("barrier")

        # Collider Component
        self.collider: Collider = self.add_component(Collider(0, 0, width, height))

        # POSITION
        self.transform.move_position(position)
