import pygame as pg
import pygame.mouse
from globals import gui_font, screen

class Button:
    def __init__(self, text, width, height, position, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = position[1]

        # Top rectangle
        self.top_rect = pg.Rect(position, (width, height))
        self.top_color = 'gray'

        # Bottom rectangle
        self.bottom_rect = pg.Rect(position, (width, elevation))
        self.bottom_color = 'darkgrey'

        # Text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # Elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pg.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = 12)
        pg.draw.rect(screen, self.top_color, self.top_rect, border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = 'lightgrey'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'