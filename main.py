from engine_JNeto_LITE.game_loop import GameLoop
from engine_JNeto_LITE.scene_and_game_objects import Scene
from game_object_player import Player
from game_object_score_manager import ScoreManager
from game_object_zombie_instantiator import ZombieInstantiator
from game_object_map import MapGrass, MapCave
from pygame import Vector2


game_loop = GameLoop()

map = MapGrass()
player = Player(initial_position=Vector2(500, 400))
zombie_instantiator_1 = ZombieInstantiator(position=Vector2(5, 530), width=20, height=220, instantiation_frequency_in_seg= 4)
zombie_instantiator_2 = ZombieInstantiator(position=Vector2(980, 5), width=287, height=20, instantiation_frequency_in_seg= 4)


main_scene = Scene(game_loop.GameSurface)
main_scene.add_game_objects(map, player, zombie_instantiator_1, zombie_instantiator_2, ScoreManager())


game_loop.run(main_scene)
