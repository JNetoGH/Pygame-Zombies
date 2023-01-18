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
        rock_1 = Barrier(position=Vector2(208, 400), width=16, height=16)
        rock_2 = Barrier(position=Vector2(593, 430), width=16, height=16)
        rock_3 = Barrier(position=Vector2(658, 271), width=16, height=16)
        wall_1 = Barrier(position=Vector2(130, 680), width=260, height=16)
        wall_2 = Barrier(position=Vector2(350, 665), width=200, height=16)
        wall_3 = Barrier(position=Vector2(510, 615), width=200, height=16)

        self.scene.add_game_objects(rock_1, rock_2, rock_3, wall_1, wall_2, wall_3)



#--------------------------------------------------------------------


class MapCave(Map):
    def __init__(self):
        super().__init__("res/map.png")

    def start(self):
        example_barrier = Barrier(position=Vector2(10, 500), width=30, height=30)
        example_barrier2 = Barrier(position=Vector2(40, 500), width=10, height=100)
        self.scene.add_game_objects(example_barrier, example_barrier2)