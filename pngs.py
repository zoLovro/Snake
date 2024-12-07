import pygame as pg
from globals import resource_path

snake_closed_mouth_right = pg.image.load(resource_path("data/pngs/snake_closed_mouth_right.png"))
snake_closed_mouth_left = pg.image.load(resource_path("data/pngs/snake_closed_mouth_left.png"))
snake_closed_mouth_up = pg.image.load(resource_path("data/pngs/snake_closed_mouth_up.png"))
snake_closed_mouth_down = pg.image.load(resource_path("data/pngs/snake_closed_mouth_down.png"))

snake_open_mouth_right = pg.image.load(resource_path("data/pngs/snake_head_mouth_right.png"))
snake_open_mouth_left = pg.image.load(resource_path("data/pngs/snake_head_mouth_left.png"))
snake_open_mouth_up = pg.image.load(resource_path("data/pngs/snake_head_mouth_up.png"))
snake_open_mouth_down = pg.image.load(resource_path("data/pngs/snake_head_mouth_down.png"))

main_menu_png = pg.image.load(resource_path("data/pngs/main-menu-bg.png"))

snake_body_col = pg.image.load(resource_path("data/pngs/snake_body.png"))
food_png = pg.image.load(resource_path("data/pngs/apple.png"))