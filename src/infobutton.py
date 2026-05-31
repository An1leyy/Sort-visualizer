"""
pygame - блиблиотека для отрисовки интерфейса.
constants - файл с константами.
"""

import pygame as pg
from src.constants import *

class InfoButton:
    """Кнопка с информацией, отображающая текст при наведении."""

    def __init__(self, x, y, normal_image_path, hover_image_path, info_text):
        self.normal_image = self.load_image(normal_image_path)
        self.hover_image = self.load_image(hover_image_path)

        self.current_image = self.normal_image
        self.rect = self.current_image.get_rect()
        self.rect.topleft = (x, y)
        self.info_text = info_text
        self.is_hovered = False
        self.tooltip_padding = 8
        self.tooltip_radius = 8
        self.tooltip_offset_x = 15
        self.tooltip_offset_y = 0
        self.font = pg.font.Font(None, INFO_FONT_SIZE)

    def load_image(self, path):
        """Загружает изображение."""

        try:
            image = pg.image.load(path).convert_alpha()
            return image
        except FileNotFoundError:
            print("File not found.")

    def create_hover_effect(self, image):
        """Создает эффект наведения."""

        hover_image = image.copy()
        hover_image.fill((255, 255, 255, 100), special_flags=pg.BLEND_RGBA_ADD)
        return hover_image

    def update(self, mouse_pos):
        """Обновляет состояние кнопки."""

        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if was_hovered != self.is_hovered:
            if self.is_hovered:
                self.current_image = self.hover_image
            else:
                self.current_image = self.normal_image

    def draw_tooltip(self, screen):
        """Рисует всплывающую подсказку."""

        if not self.is_hovered:
            return

        lines = self.info_text.split('\n')
        line_height = INFO_LINE_HEIGHT

        max_width = 0
        for line in lines:
            text_surface = self.font.render(line, True, INFO_TEXT_COLOR)
            max_width = max(max_width, text_surface.get_width())

        tooltip_width = max_width + self.tooltip_padding * 2
        tooltip_height = len(lines) * line_height + self.tooltip_padding * 2

        tooltip_x = self.rect.right + self.tooltip_offset_x
        tooltip_y = self.rect.centery - tooltip_height // 2 + self.tooltip_offset_y

        if tooltip_x + tooltip_width > screen.get_width():
            tooltip_x = self.rect.left - tooltip_width - self.tooltip_offset_x

        if tooltip_y < 0:
            tooltip_y = 0
        if tooltip_y + tooltip_height > screen.get_height():
            tooltip_y = screen.get_height() - tooltip_height

        pg.draw.rect(
            screen,
            INFO_BG_COLOR,
            (tooltip_x, tooltip_y, tooltip_width, tooltip_height),
            border_radius=self.tooltip_radius
        )

        pg.draw.rect(
            screen,
            INFO_BORDER_COLOR,
            (tooltip_x, tooltip_y, tooltip_width, tooltip_height),
            width=2,
            border_radius=self.tooltip_radius
        )

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, INFO_TEXT_COLOR)
            text_rect = text_surface.get_rect(
                topleft=(
                    tooltip_x + self.tooltip_padding,
                    tooltip_y + self.tooltip_padding + i * line_height
                )
            )
            screen.blit(text_surface, text_rect)

    def draw(self, screen):
        """Рисует кнопку и подсказку."""

        screen.blit(self.current_image, self.rect)
        self.draw_tooltip(screen)
