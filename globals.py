import pygame as pg
import sys
import os

WINDOW = 750
TILE_SIZE = 50
screen = pg.display.set_mode([WINDOW] * 2)

# Fonts
pg.font.init()
gui_font = pg.font.Font('Data/Grand9K_Pixel.ttf', 30)
menu_font = pg.font.Font('Data/Grand9K_Pixel.ttf', 150)
over_font = pg.font.Font('Data/Grand9K_Pixel.ttf', 100)

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for PyInstaller. """
    if hasattr(sys, '_MEIPASS'):
        # When bundled as an executable, resources are extracted to `_MEIPASS`
        return os.path.join(sys._MEIPASS, relative_path)
    # When running as a script, resources are accessed normally
    return os.path.join(os.path.abspath("."), relative_path)