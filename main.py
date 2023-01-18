from engine_JNeto_LITE.game_loop import GameLoop
from engine_JNeto_LITE.scene_and_game_objects import Scene
from game_objects.game_object_player import Player
from game_objects.game_object_buttons import ButtonManager
from game_objects.game_object_score_manager import ScoreManager
from game_objects.game_object_zombie_instantiator import ZombieInstantiator
from game_objects.game_object_map import MapGrass
from pygame import Vector2


"""
JOÃO NETO (a22200558): 
Responsável geral e líder de projeto, trabalhei na criação da engine e core mechanincs do game, 
tais quais as ilustradas no documento pdf enviado juntamente ao projeto, tendo com base a implementação
puramente matemática nos mais diversos aspectos do game.

DAVID MENDES (A22203255):
Dev Axuliar, esteve ao lado em todas as decisões, ajudou a co-criar o sistema de colisões, foi o responsável
pelas artes do jogo, e game design, tendo importancia primordial no refinamento dos parâmetros utilizados dentro 
do game tanto para fins matemáticos quantos de simulação física.
"""


game_loop = GameLoop()

map = MapGrass()
player = Player(initial_position=Vector2(500, 400))
zombie_instantiator_1 = ZombieInstantiator(position=Vector2(5, 530), width=20, height=220, instantiation_frequency_in_seg= 4)
zombie_instantiator_2 = ZombieInstantiator(position=Vector2(980, 5), width=287, height=20, instantiation_frequency_in_seg= 4)
button_manager = ButtonManager()

main_scene = Scene(game_loop.GameSurface)
main_scene.add_game_objects(map, player, zombie_instantiator_1, zombie_instantiator_2, ScoreManager(), button_manager)


game_loop.run(main_scene)
