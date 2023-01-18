from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import Scene
from game_object_player import Player
from game_object_zombie import Zombie
from pygame import Vector2

game_loop = GameLoop()

main_scene = Scene(game_loop.game_surface)
main_scene.add_game_objects(Player(), Zombie(Vector2(100, 100)), Zombie(Vector2(1000, 400)), Zombie(Vector2(400, 600)))

game_loop.run(main_scene)
