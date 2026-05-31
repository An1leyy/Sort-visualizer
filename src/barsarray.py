"""
bar - объект колонки
"""

from src.bar import *

class BarsArray:
    """Массив колонок, визуализирующий операции над ними."""

    def __init__(self, array):
        self.bars_array = []
        self.max_val = max(array)
        self.min_val = min(array)
        self.bar_width = round(
            (I_WIDTH - (I_SPACE * 2) - (SPACE_BETWEEN_BARS * len(array))) / len(array)
            )

        for i, value in enumerate(array):
            self.bars_array.append(Bar(
                I_POSX + I_SPACE + (self.bar_width + SPACE_BETWEEN_BARS) * i,
                self.bar_width,
                get_bar_height(value, self.min_val, self.max_val, BAR_MIN_HEIGHT, BAR_MAX_HEIGHT),
                value
    ))

    def draw(self, screen):
        """Рисует все колонки из массива."""

        for i in self.bars_array:
            i.draw(screen)

    def update(self, delta_time):
        """Обновляет состояние массива."""

        for i in self.bars_array:
            i.update(delta_time)

    def highlight_bars(self, index_a, index_b):
        """Подсвечивает две колонки в массиве."""

        bar_a = self.bars_array[index_a]
        bar_b = self.bars_array[index_b]

        bar_a.highlight()
        bar_b.highlight()

    def swap_bars(self, index_a, index_b):
        """Меняет колонки в массиве местами."""

        if (
            index_a == index_b) or (not (0 <= index_a < len(self.bars_array))
        ) or (
            not (0 <= index_b < len(self.bars_array))
        ):
            return False

        bar_a = self.bars_array[index_a]
        bar_b = self.bars_array[index_b]

        bar_a.move_to_index(index_a, index_b)
        bar_b.move_to_index(index_b, index_a)

        self.bars_array[index_a], self.bars_array[index_b] = \
            self.bars_array[index_b], self.bars_array[index_a]

        return True

    def is_animating(self):
        """Проверяет, анимируется ли массив."""

        return any(i.is_animating() for i in self.bars_array)
    