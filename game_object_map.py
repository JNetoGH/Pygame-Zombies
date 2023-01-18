from JNeto_engine_lite.components import Sprite
from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import GameObject
from pygame import Vector2
from game_object_barrier import Barrier


class Map(GameObject):
    def __init__(self, path_to_image: str):
        super().__init__("map")
        # position
        resolution = GameLoop.RESOLUTION
        self.transform.move_position(Vector2(resolution[0]//2, resolution[1]//2))
        # sprite
        self.sprite = self.add_component(Sprite(path_to_image))


#--------------------------------------------------------------------


class MapGrass(Map):
    def __init__(self):
        super().__init__("res/map.png")

    def start(self):
        rock_1 = Barrier(position=Vector2(525, 300), width=25, height=25)
        rock_2 = Barrier(position=Vector2(593, 430), width=25, height=25)
        stump_1 = Barrier(position=Vector2(880, 270), width=25, height=25)
        stump_2 = Barrier(position=Vector2(305, 525), width=25, height=25)
        wall_1 = Barrier(position=Vector2(130, 680), width=260, height=25)
        wall_2 = Barrier(position=Vector2(355, 650), width=200, height=25)
        wall_3 = Barrier(position=Vector2(500, 615), width=200, height=25)
        wall_4 = Barrier(position=Vector2(613, 565), width=150, height=50)
        wall_5 = Barrier(position=Vector2(613, 555), width=100, height=25)

        self.scene.add_game_objects(rock_1, rock_2, stump_1, stump_2, wall_1, wall_2, wall_3, wall_4)



#--------------------------------------------------------------------


class MapCave(Map):
    def __init__(self):
        super().__init__("res/map.png")

    def start(self):
        example_barrier = Barrier(position=Vector2(10, 500), width=30, height=30)
        example_barrier2 = Barrier(position=Vector2(40, 500), width=10, height=100)
        self.scene.add_game_objects(example_barrier, example_barrier2)