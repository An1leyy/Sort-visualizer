import pygame as pg

class Button:
    def __init__(self, x, y, normal_image, pressed_image=None):
        self.normal_image = self.load_and_scale(normal_image)
        self.pressed_image = self.load_and_scale(pressed_image) if pressed_image else self.normal_image
        
        self.current_image = self.normal_image
        self.rect = self.current_image.get_rect()
        self.rect.topleft = (x, y)
        
        self.is_pressed = False
        
    def load_and_scale(self, path):
        image = pg.image.load(path).convert_alpha()
        return image
    
    def update(self):
        if self.is_pressed:
            self.current_image = self.pressed_image
        else:
            self.current_image = self.normal_image
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return False
                
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.rect.collidepoint(event.pos):
                    return True
        return False
    
    def draw(self, screen):
        screen.blit(self.current_image, self.rect)