import pygame
from pygame import Color, font, Vector2, Surface
pygame.init()

# ------------------------------------------

# MY_FONT

FONT_SIZE: int = 20
FONT_PATH: str = "engine_JNeto_LITE/JetBrainsMono-Medium.ttf"
MY_FONT: font.Font = font.Font(FONT_PATH, FONT_SIZE)

# ------------------------------------------

# COLORS

WHITE = Color(255, 255, 255)
GREY = Color(128, 128, 128)

RED_PASTEL = Color(255, 105, 97)
PINK_PASTEL = Color(244, 154, 194)
GREEN_PASTEL = Color(190, 229, 179)
YELLOW_PASTEL = Color(248, 241, 174)
CYAN_PASTEL = Color(128, 206, 255)
ORANGE_PASTEL = Color(255, 179, 71)

DARK_RED_PASTEL = Color(170, 67, 68)

# ------------------------------------------

# GIZMOS

GIZMOS_WIDTH = 2
GIZMOS_LINE_LENGTH = 100
# gizmos caching (texs intantiations are to have in pygame, so i am caching them all)
CACHED_0_ANGLE_TEXT = MY_FONT.render("0º", True, YELLOW_PASTEL, None)
CACHED_ANGLES_TEXTS = [MY_FONT.render(f"{i}º", True, PINK_PASTEL, None) for i in range(0, 361)]


def draw_special_gizmos(game_surface: Surface, position: Vector2, direction: Vector2, angle) -> None:
    # 0ª line
    end = position + Vector2(0, -1) * GIZMOS_LINE_LENGTH
    pygame.draw.line(game_surface, YELLOW_PASTEL, position, end, GIZMOS_WIDTH)
    end.x += 5
    game_surface.blit(CACHED_0_ANGLE_TEXT, end)
    # direction
    end_player_dir = position + direction * GIZMOS_LINE_LENGTH
    pygame.draw.line(game_surface, PINK_PASTEL, position, end_player_dir, GIZMOS_WIDTH)
    game_surface.blit(CACHED_ANGLES_TEXTS[int(angle)], end_player_dir)


def get_converted_angle_to_0_360_range(angle):
    # 0 + what passed from 360
    if angle > 360:
        angle = angle - 360
    # 360 - what passed from 0
    elif angle < 0:
        angle = 360 - (angle * -1)
    return angle