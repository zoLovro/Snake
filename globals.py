import pygame as pg

WINDOW = 750
TILE_SIZE = 50
screen = pg.display.set_mode([WINDOW] * 2)

pg.font.init()

gui_font = pg.font.Font('Grand9K Pixel.ttf', 30)
menu_font = pg.font.Font('Grand9K Pixel.ttf', 150)
over_font = pg.font.Font('Grand9K Pixel.ttf', 100)
