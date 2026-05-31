"""
pygame - блиблиотека для отрисовки интерфейса.
"""

import pygame as pg

class Button:
    """
    Кнопка для взаимодействия
    с интерфейсом.
    """

    def __init__(self, x, y, normal_image, pressed_image=None):
        self.normal_image = self.load_and_scale(normal_image)
        self.pressed_image = self.load_and_scale(pressed_image) \
        if pressed_image else self.normal_image

        self.disabled_image = self.create_disabled_image(self.normal_image)

        self.current_image = self.normal_image
        self.rect = self.current_image.get_rect()
        self.rect.topleft = (x, y)

        self.is_pressed = False
        self.is_enabled = True

    def load_and_scale(self, path):
        """Загружает и возвращает текстуру кнопки."""
        try:
            image = pg.image.load(path).convert_alpha()
            return image
        except FileNotFoundError:
            print("File not found.")

    def create_disabled_image(self, image):
        """
        Создает затемненную версию изображения для недоступного состояния.
        """
        disabled_image = image.copy()

        for x in range(disabled_image.get_width()):
            for y in range(disabled_image.get_height()):
                color = disabled_image.get_at((x, y))
                if color.a > 0:
                    darker_color = (color[0] // 2, color[1] // 2, color[2] // 2, color[3])
                    disabled_image.set_at((x, y), darker_color)

        return disabled_image

    def set_enabled(self, enabled):
        """
        Устанавливает доступность кнопки.
        """

        self.is_enabled = enabled
        self.update()

        if not enabled:
            self.is_pressed = False

    def is_button_enabled(self):
        """Возвращает доступна ли кнопка."""

        return self.is_enabled

    def update(self):
        """Обновляет состояние кнопки."""

        if not self.is_enabled:
            self.current_image = self.disabled_image
        elif self.is_pressed:
            self.current_image = self.pressed_image
        else:
            self.current_image = self.normal_image

    def handle_event(self, event):
        """Проверяет, нажата ли кнопка."""

        if not self.is_enabled:
            return False

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
        """Рисует кнопку."""

        screen.blit(self.current_image, self.rect)
