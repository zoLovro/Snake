import pygame as pg
from pngs import (snake_body_col, snake_open_mouth_right, snake_open_mouth_left, snake_open_mouth_up, snake_open_mouth_down,
                  snake_closed_mouth_right, snake_closed_mouth_left, snake_closed_mouth_up, snake_closed_mouth_down)

state_mapping = {
    snake_closed_mouth_right: snake_open_mouth_right,
    snake_open_mouth_right: snake_closed_mouth_right,
    snake_closed_mouth_left: snake_open_mouth_left,
    snake_open_mouth_left: snake_closed_mouth_left,
    snake_closed_mouth_up: snake_open_mouth_up,
    snake_open_mouth_up: snake_closed_mouth_up,
    snake_closed_mouth_down: snake_open_mouth_down,
    snake_open_mouth_down: snake_closed_mouth_down,
    }