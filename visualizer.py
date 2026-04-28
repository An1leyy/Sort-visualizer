import pygame as pg
import sys
import random
import os
from constants import *
from barsarray import BarsArray
from sorts import *
from button import Button

class Visualizer:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Sort visualizer")
        self.clock = pg.time.Clock()
        
        self.baseArray = []
        self.copyArray = self.baseArray.copy()
        self.actions = []
        self.current_action_index = 0
        if len(self.baseArray) == 0:
            self.baseArray = [random.randint(ARRAY_MIN_ELEMENT, ARRAY_MAX_ELEMENT) for _ in range(random.randint(10, ARRAY_SIZE_LIMIT))]
            self.reset_bars()
            self.is_sorting = False
            self.actions = []
            self.current_action_index = 0
        self.bars_Array = BarsArray(self.baseArray)
        
        self.waiting_for_animation = False
        self.automode = False

        self.sorttype = "Bubble"
        self.start_sorting(bubble_sort_rec)
    
    def start_sorting(self, sort_algorithm):
        self.actions = []
        self.copyArray = self.baseArray.copy()
        
        sort_algorithm(self.copyArray, self.actions)
        
        self.current_action_index = 0
        self.waiting_for_animation = False
        self.reset_bars()
    
    def reset_bars(self):
        self.bars_Array = BarsArray(self.baseArray)
    
    def execute_next_action(self):
        if self.current_action_index >= len(self.actions):
            return False
        
        action = self.actions[self.current_action_index]
        self.current_action_index += 1
        
        if action[0] == 'swap':
            _, i, j = action
            self.bars_Array.swap_bars(i, j)
            
        elif action[0] == 'compare':
            _, i, j = action
            self.bars_Array.highlight_bars(i, j)
        
        return True

    def import_array_from_file(self):
        file_path = "files/array.txt"
        
        array, error_message = self.read_array_from_file(file_path)
        
        if error_message:
            self.show_error_message(error_message)
            return
        
        self.baseArray = array
        self.start_sorting(SORT_ALGORITHMS.get(self.sorttype))
        self.automode = False
    
    def read_array_from_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                self.create_default_array_file(file_path)
                return None, f"File {file_path} not found.\nCreated new file at {file_path}."
            
            with open(file_path, 'r', encoding='utf-8') as file:
                first_line = file.readline()
                second_line = file.readline().strip()
                
                if not second_line:
                    return None, "The file does not contain an array.\nEnter your array on the second line of the file."
            
            array = self.parse_numbers_line(second_line)
            
            if array is None:
                return None, "Uncorrect data format.\nUse format: 1 2 3 4 5"
            
            is_valid, error_message = self.validate_array(array)
            
            if not is_valid:
                return None, error_message
            
            return array, None
            
        except Exception as e:
            return None, f"File reading error: {str(e)}"
    
    def parse_numbers_line(self, line):
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
        if not array:
            return False, "Array is empty! Enter at least one number"
        
        if len(array) > 35:
            return False, f"Too much elements ({len(array)}).\nMaximum length of the array is 35."
    
        for i, value in enumerate(array):
            if value > 1000:
                return False, f"Element at index {i+1} ({value}) larger than 1000.\nMaximum possible number is 1000."
            if value < -999:
                return False, f"Element at index {i+1} ({value}) lower than -999.\nMinimum possible number is -999."
        
        return True, None

    def show_error_message(self, message):
        self.error_message = message
        self.error_message_timer = FPS * 3
    
    def draw_messages(self):
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

    def create_default_array_file(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("Write the array on the next line in the format \"1 2 3 4 5 6 7\", the maximum length of the array is 35, the maximum possible number is 1000, the minimum is -999.\n")
        except Exception as e:
            print(f"File creating error: {e}")

    def run(self):
        running = True
        last_time = pg.time.get_ticks() / 1000.0

        self.playbutton = Button(465, 502, "textures/playbutton.png", "textures/playbuttonact.png")
        self.pausebutton = Button(465, 502, "textures/pausebutton.png", "textures/pausebuttonact.png")
        self.restartbutton = Button(371, 512, "textures/restartbutton.png", "textures/restartbuttonact.png")
        self.stepbutton = Button(578, 512, "textures/stepbutton.png", "textures/stepbuttonact.png")
        self.leftbutton = Button(84, 523, "textures/leftarrow.png")
        self.rightbutton = Button(256, 523, "textures/rightarrow.png")
        self.randombutton = Button(797, 512, "textures/randombutton.png", "textures/randombuttonact.png")
        self.exitbutton = Button(869, 20, "textures/exitbutton.png", "textures/exitbuttonact.png")
        self.importbutton = Button(27, 20, "textures/importbutton.png", "textures/importbuttonact.png")

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

        while running:
            current_time = pg.time.get_ticks() / 1000.0
            delta_time = current_time - last_time
            last_time = current_time
            delta_time = min(delta_time, 1 / FPS)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                    if (self.automode and self.pausebutton.handle_event(event)) or (not self.automode and self.playbutton.handle_event(event)):
                        self.automode = not self.automode

                    if self.stepbutton.handle_event(event):
                        if self.current_action_index != (len(self.actions)) and self.waiting_for_animation == False and self.automode == False:
                            self.execute_next_action()

                    if self.restartbutton.handle_event(event):
                        self.current_action_index = 0
                        self.waiting_for_animation = False
                        self.reset_bars()

                    if self.randombutton.handle_event(event):
                        self.baseArray = [random.randint(ARRAY_MIN_ELEMENT, ARRAY_MAX_ELEMENT) for _ in range(random.randint(10, ARRAY_SIZE_LIMIT))]
                        self.start_sorting(SORT_ALGORITHMS.get(self.sorttype))
                        self.automode = False

                    if self.exitbutton.handle_event(event):
                        running = False

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
                        running = False

                    if event.key == pg.K_r:
                        self.baseArray = [random.randint(ARRAY_MIN_ELEMENT, ARRAY_MAX_ELEMENT) for _ in range(random.randint(10, ARRAY_SIZE_LIMIT))]
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
                        if self.current_action_index != (len(self.actions)) and self.waiting_for_animation == False and self.automode == False:
                            self.execute_next_action()

                    if event.key == pg.K_a:
                        self.automode = not self.automode
            
            if self.automode == True and self.current_action_index != (len(self.actions)) and self.waiting_for_animation == False:
                self.execute_next_action()
            
            self.bars_Array.update(delta_time)

            self.waiting_for_animation = self.bars_Array.is_animating()
            
            self.screen.fill(GREYBG)
            pg.draw.rect(self.screen, I_GREY, (50, 85, I_WIDTH, I_HEIGHT), border_radius=10)
            pg.draw.rect(self.screen, I_GREY, (115, 518, 130, 38), border_radius=10)
            
            self.bars_Array.draw(self.screen)
            
            font = pg.font.Font(None, 15)
            font2 = pg.font.Font(None, 30)
            info_text = f"Step: {self.current_action_index}/{len(self.actions)} | B-Bubble I-Insertion S-Selection | R-New array | SPACE-Step | A-Automode: {'ON' if self.automode else 'OFF'}"
            text = font.render(info_text, True, WHITE)
            self.screen.blit(text, (10, HEIGHT - 10))

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

            for button in self.buttons:
                if button == self.playbutton and self.automode:
                    continue
                if button == self.pausebutton and not self.automode:
                    continue
                button.draw(self.screen)
            
            self.draw_messages()
            
            pg.display.flip()
            self.clock.tick(FPS)
            
        pg.quit()
        sys.exit()