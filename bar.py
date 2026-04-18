import pygame as pg
from constants import *

class Bar:
    def __init__(self, x, width, height, value):
        self.x = x
        self.y = BARS_Y_BORDER
        self.width = width
        self.height = -1 * height
        self.value = value
        self.color = BARCOLOR
        self.target_x = x

        self.target_x = x
        self.start_x = x
        self.move_timer = 0.0
        self.highlight_timer = 0.0
        self.is_moving = False
        self.is_highlighted = False
        self.font = pg.font.Font(None, TEXT_FONT_SIZE)
        
    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=5)

        self.draw_value(screen)
    
    def draw_value(self, screen):
        value_str = str(self.value)

        if self.value > 0:
            text_color = GREEN
        elif self.value < 0:
            text_color = RED
        else:
            text_color = WHITE
        
        text_surface = self.font.render(value_str, True, text_color)
        rotated_surface = pg.transform.rotate(text_surface, 90)
        
        text_x = self.x + self.width // 2 - rotated_surface.get_width() // 2
        text_y = self.y + TEXT_VERTICAL_OFFSET
        
        bg_width = rotated_surface.get_width() + TEXT_BG_SPACE * 2
        bg_height = rotated_surface.get_height() + TEXT_BG_SPACE * 2
        bg_surface = pg.Surface((bg_width, bg_height), pg.SRCALPHA)
        
        pg.draw.rect(bg_surface, (*BLACK, TEXT_BG_ALPHA), (0, 0, bg_width, bg_height), border_radius=5)
        screen.blit(bg_surface, (text_x - TEXT_BG_SPACE, text_y - TEXT_BG_SPACE))
        screen.blit(rotated_surface, (text_x, text_y))
    
    def move_to_index(self, current_index, target_index):
        self.target_x = self.x + ((target_index - current_index) * (self.width + SPACE_BETWEEN_BARS))
        
        self.start_x = self.x
        self.move_timer = 0.0
        self.is_moving = True
    
    def highlight(self):
        self.highlight_timer = 0.0
        self.is_highlighted = True
    
    def update(self, delta_time):
        if self.is_moving:
            self.move_timer += delta_time
            
            progress = min(1.0, self.move_timer / BAR_ACTION_TIME)
            
            self.x = self.start_x + (self.target_x - self.start_x) * progress
            
            if progress >= 1.0:
                self.x = self.target_x
                self.is_moving = False
        
        if self.is_highlighted:
            self.highlight_timer += delta_time

            self.color = BARHIGHLIGHTCOLOR

            progress = min(1.0, self.highlight_timer / BAR_ACTION_TIME)

            if progress >= 1.0:
                self.color = BARCOLOR
                self.is_highlighted = False
    
    def is_animating(self):
        return self.is_moving or self.is_highlighted

def get_bar_height(value, min_value, max_value, min_height=BAR_MIN_HEIGHT, max_height=BAR_MAX_HEIGHT):
    if min_value == max_value:
        return (min_height + max_height) // 2
    height = min_height + (value - min_value) * (max_height - min_height) / (max_value - min_value)
    return int(round(height))