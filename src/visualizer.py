"""
pygame - блиблиотека для отрисовки интерфейса.
sys, os - управление системными командами.
random - генерация случайных значений.
constants - файл с константами.
BarsArray - объект массива столбцов.
ArrayConfigManager - объект для импорта данных из json файла.
sorts - файл с алгоритмами сортировок.
Button - объект кнопки.
tkinter - управление файлами.
"""

import pygame as pg
import sys
import random
import os
from src.constants import *
from src.barsarray import BarsArray
from src.sorts import *
from src.button import Button
from src.infobutton import InfoButton
import tkinter as tk
from tkinter import filedialog
from src.arrayconfigmanager import ArrayConfigManager

class Visualizer:
    """Основной класс визуализатора."""

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Sort visualizer")
        self.clock = pg.time.Clock()
        self.running = False

        self.base_array = []
        self.copy_array = self.base_array.copy()
        self.actions = []
        self.current_action_index = 0
        self.array_config_manager = ArrayConfigManager()
        if len(self.base_array) == 0:
            self.generate_random_array()
            self.reset_bars()
            self.is_sorting = False
            self.actions = []
            self.current_action_index = 0
        self.bars_array = BarsArray(self.base_array)

        self.waiting_for_animation = False
        self.automode = False

        self.sorttype = "Bubble"
        self.start_sorting(bubble_sort_rec)

        self.playbutton = Button(465, 502, "textures/playbutton.png", "textures/playbuttonact.png")
        self.pausebutton = Button(465, 502, "textures/pausebutton.png", "textures/pausebuttonact.png")
        self.restartbutton = Button(371, 512, "textures/restartbutton.png", "textures/restartbuttonact.png")
        self.stepbutton = Button(578, 512, "textures/stepbutton.png", "textures/stepbuttonact.png")
        self.leftbutton = Button(84, 523, "textures/leftarrow.png")
        self.rightbutton = Button(256, 523, "textures/rightarrow.png")
        self.randombutton = Button(797, 512, "textures/randombutton.png", "textures/randombuttonact.png")
        self.exitbutton = Button(869, 20, "textures/exitbutton.png", "textures/exitbuttonact.png")
        self.importbutton = Button(27, 20, "textures/importbutton.png", "textures/importbuttonact.png")

        self.infobutton = InfoButton(17, 539, "textures/info.png", "textures/infoac.png",\
        'B-Bubble I-Insertion S-Selection\nR-New array\nSPACE-Step\nA-Automode switch\nESC-Exit')

        self.buttons = [
            self.playbutton,
            self.pausebutton,
            self.restartbutton,
            self.stepbutton,
            self.leftbutton,
            self.rightbutton,
            self.randombutton,
            self.exitbutton,
            self.importbutton
        ]

        self.error_message = ''
        self.error_message_timer = 0

    def generate_random_array(self):
        """Генерирует случайный массив на основе JSON параметров или констант."""

        params = self.array_config_manager.get_generation_params()
        if params and self.array_config_manager.validate_params(params):
            min_length = params["min_length"]
            max_length = params["max_length"]
            min_element = params["min_element"]
            max_element = params["max_element"]

            size = random.randint(min_length, max_length)
            self.base_array = [
                random.randint(min_element, max_element)
                for _ in range(size)
            ]
        else:
            size = random.randint(10, ARRAY_SIZE_LIMIT)
            self.base_array = [
                random.randint(ARRAY_MIN_ELEMENT, ARRAY_MAX_ELEMENT)
                for _ in range(size)
            ]

        self.reset_bars()
        self.is_sorting = False
        self.actions = []
        self.current_action_index = 0
        self.automode = False

    def start_sorting(self, sort_algorithm):
        """Начало сортировки массива."""

        self.actions = []
        self.copy_array = self.base_array.copy()

        sort_algorithm(self.copy_array, self.actions)

        self.current_action_index = 0
        self.waiting_for_animation = False
        self.reset_bars()

    def reset_bars(self):
        """Сбрасывает позицию всех столбцов массива"""

        self.bars_array = BarsArray(self.base_array)

    def execute_next_action(self):
        """
        Выполняет следующее действие,
        указанное в списке actions.
        """

        if self.current_action_index >= len(self.actions):
            return False

        action = self.actions[self.current_action_index]
        self.current_action_index += 1

        if action[0] == 'swap':
            _, i, j = action
            self.bars_array.swap_bars(i, j)

        elif action[0] == 'compare':
            _, i, j = action
            self.bars_array.highlight_bars(i, j)

        return True

    def import_array_from_file(self):
        """Импортирует массив из выбранного пользователем файла."""

        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Выберите файл с массивом",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            initialdir=os.path.expanduser("~")
        )

        root.destroy()

        if not file_path:
            self.show_error_message("File selection cancelled.")
            return

        array, error_message = self.read_array_from_file(file_path)

        if error_message:
            self.show_error_message(error_message)
            return

        self.base_array = array
        self.start_sorting(SORT_ALGORITHMS.get(self.sorttype))
        self.automode = False


    def read_array_from_file(self, file_path):
        """Читает массив из выбранного файла."""

        try:
            if not os.path.exists(file_path):
                return None, f"File not found: {file_path}"

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()

            if not content:
                return None, "The file is empty.\nEnter numbers separated by spaces on the first line."

            lines = content.split('\n')
            array_line = None

            for line in lines:
                line = line.strip()
                if line and not line.startswith(('#', '//', 'Write', 'Запишите')):
                    parts = line.split()
                    if parts and any(part.lstrip('-').replace('.', '').isdigit() for part in parts):
                        array_line = line
                        break

            if not array_line:
                return None, "No numbers found in file.\nUse format: 1 2 3 4 5"

            array = self.parse_numbers_line(array_line)

            if array is None:
                return None, "Invalid data format.\nUse format: 1 2 3 4 5"

            is_valid, error_message = self.validate_array(array)

            if not is_valid:
                return None, error_message

            return array, None

        except FileNotFoundError as e:
            return None, f"File reading error: {str(e)}"

    def parse_numbers_line(self, line):
        """Парсит массив из файла."""

        parts = line.split()

        if not parts:
            return None
        array = []
        for part in parts:
            try:
                num = int(part)
                array.append(num)
            except ValueError:
                try:
                    num = float(part)
                    array.append(int(num))
                except ValueError:
                    return None

        return array

    def validate_array(self, array):
        """Проверяет массив на корректность."""

        if not array:
            return False, "Array is empty! Enter at least one number"

        if len(array) > ARRAY_SIZE_LIMIT:
            return False, f"Too much elements ({len(array)}).\n\
                Maximum length of the array is {ARRAY_SIZE_LIMIT}."

        return True, None

    def show_error_message(self, message):
        """Определяет выводимое сообщение об ошибке."""

        self.error_message = message
        self.error_message_timer = FPS * 3

    def draw_messages(self):
        """Рисует сообщение об ошибке."""

        font = pg.font.Font(None, 20)

        if hasattr(self, 'error_message_timer') and self.error_message_timer > 0:
            lines = self.error_message.split('\n')
            line_height = 15
            padding = 5
            corner_radius = 10

            max_width = 0
            for line in lines:
                text_surface = font.render(line, True, RED)
                max_width = max(max_width, text_surface.get_width())

            square_width = max_width + padding * 2
            square_height = len(lines) * line_height + padding * 2
            square_x = ERROR_MESSAGE_X
            square_y = ERROR_MESSAGE_Y

            pg.draw.rect(
                self.screen,
                BLACK,
                (square_x, square_y, square_width, square_height),
                border_radius=corner_radius
            )
            pg.draw.rect(
                self.screen,
                RED,
                (square_x, square_y, square_width, square_height),
                width=2,
                border_radius=corner_radius
            )

            for i, line in enumerate(lines):
                text_surface = font.render(line, True, RED)
                text_rect = text_surface.get_rect(
                    topleft=(ERROR_MESSAGE_X + padding, ERROR_MESSAGE_Y + padding + i * line_height)
                )
                self.screen.blit(text_surface, text_rect)

            self.error_message_timer -= 1
            if self.error_message_timer <= 0:
                delattr(self, 'error_message_timer')

    def event_handler(self):
        """Обработчик событий."""

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                if (self.automode and self.pausebutton.handle_event(event))\
                    or (not self.automode and self.playbutton.handle_event(event)):
                    self.automode = not self.automode

                if self.stepbutton.handle_event(event):
                    if self.current_action_index != (len(self.actions))\
                        and not self.waiting_for_animation and not self.automode:
                        self.execute_next_action()

                if self.restartbutton.handle_event(event):
                    self.current_action_index = 0
                    self.waiting_for_animation = False
                    self.reset_bars()

                if self.randombutton.handle_event(event):
                    self.generate_random_array()
                    self.start_sorting(SORT_ALGORITHMS.get(self.sorttype))
                    self.automode = False

                if self.exitbutton.handle_event(event):
                    self.running = False

                if self.importbutton.handle_event(event):
                    self.import_array_from_file()

                if self.leftbutton.handle_event(event):
                    current_index = SORT_TYPES.index(self.sorttype)
                    new_index = (current_index - 1) % len(SORT_TYPES)
                    self.sorttype = SORT_TYPES[new_index]
                    self.start_sorting(SORT_ALGORITHMS.get(self.sorttype))

                if self.rightbutton.handle_event(event):
                    current_index = SORT_TYPES.index(self.sorttype)
                    new_index = (current_index + 1) % len(SORT_TYPES)
                    self.sorttype = SORT_TYPES[new_index]
                    self.start_sorting(SORT_ALGORITHMS.get(self.sorttype))

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

                if not self.automode:
                    if event.key == pg.K_r:
                        self.generate_random_array()
                        self.start_sorting(SORT_ALGORITHMS.get(self.sorttype))
                        self.automode = False

                    if event.key == pg.K_b:
                        self.sorttype = "Bubble"
                        self.start_sorting(bubble_sort_rec)

                    if event.key == pg.K_i:
                        self.sorttype = "Insertion"
                        self.start_sorting(insertion_sort_rec)

                    if event.key == pg.K_s:
                        self.sorttype = "Selection"
                        self.start_sorting(selection_sort_rec)

                    if event.key == pg.K_SPACE:
                        if self.current_action_index != (len(self.actions))\
                            and not self.waiting_for_animation and not self.automode:
                            self.execute_next_action()

                if event.key == pg.K_a:
                    self.automode = not self.automode

    def run(self):
        """Основной цикл программы."""

        self.running = True
        last_time = pg.time.get_ticks() / 1000.0

        while self.running:
            current_time = pg.time.get_ticks() / 1000.0
            delta_time = current_time - last_time
            last_time = current_time
            delta_time = min(delta_time, 1 / FPS)
            mouse_pos = pg.mouse.get_pos()

            self.event_handler()

            if self.automode and self.current_action_index != (len(self.actions))\
                and not self.waiting_for_animation:
                self.execute_next_action()

            self.bars_array.update(delta_time)

            self.waiting_for_animation = self.bars_array.is_animating()

            self.screen.fill(GREYBG)
            pg.draw.rect(self.screen, I_GREY, (50, 85, I_WIDTH, I_HEIGHT), border_radius=10)
            pg.draw.rect(self.screen, I_GREY, (115, 518, 130, 38), border_radius=10)

            self.bars_array.draw(self.screen)

            font = pg.font.Font(None, 25)
            font2 = pg.font.Font(None, 30)
            info_text = f"Step: {self.current_action_index}/{len(self.actions)}"
            text = font.render(info_text, True, WHITE)
            self.screen.blit(text, (10, HEIGHT - 20))

            text_area_x = 115
            text_area_y = 527
            text_area_width = 130

            sort_text = f"{self.sorttype}"

            text2 = font2.render(sort_text, True, WHITE)

            text_x = text_area_x + (text_area_width - text2.get_width()) // 2
            text_y = text_area_y

            self.screen.blit(text2, (text_x, text_y))

            for button in self.buttons:
                button.update()

            self.infobutton.update(mouse_pos)

            for button in self.buttons:
                if button == self.playbutton and self.automode:
                    continue
                if button == self.pausebutton and not self.automode:
                    continue
                if button != self.playbutton and button != self.pausebutton and button != self.exitbutton and self.automode:
                    button.set_enabled(False)
                if button != self.playbutton and button != self.pausebutton and button != self.exitbutton and not self.automode:
                    button.set_enabled(True)
                button.draw(self.screen)

            self.infobutton.draw(self.screen)

            self.draw_messages()

            pg.display.flip()
            self.clock.tick(FPS)

        pg.quit()
        sys.exit()
