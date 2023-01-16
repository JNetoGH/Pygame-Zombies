from JNeto_engine_lite.game_loop import GameLoop
from JNeto_engine_lite.scene_and_game_objects import Scene
from player import Player

game_loop = GameLoop()

main_scene = Scene(game_loop.game_surface)
main_scene.add_game_object(Player())
game_loop.run(main_scene)