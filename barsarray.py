from bar import *

class BarsArray:
    def __init__(self, array):
        self.barsArray = []
        self.max_val = max(array)
        self.min_val = min(array)
        self.barWidth = round((I_WIDTH - (I_SPACE * 2) - (SPACE_BETWEEN_BARS * len(array))) / len(array))
        
        for i in range(0, len(array)):
            self.barsArray.append(Bar(I_POSX + I_SPACE + (self.barWidth + SPACE_BETWEEN_BARS) * i,
            self.barWidth, get_bar_height(array[i], self.min_val, self.max_val, BAR_MIN_HEIGHT, BAR_MAX_HEIGHT), array[i]))
    
    def draw(self, screen):
        for i in self.barsArray:
            i.draw(screen)
    
    def update(self, delta_time):
        for bar in self.barsArray:
            bar.update(delta_time)
    
    def highlight_bars(self, index_a, index_b):
        bar_a = self.barsArray[index_a]
        bar_b = self.barsArray[index_b]
        
        bar_a.highlight()
        bar_b.highlight()
    
    def swap_bars(self, index_a, index_b):
        if (index_a == index_b) or (not (0 <= index_a < len(self.barsArray))) or (not (0 <= index_b < len(self.barsArray))):
            return False
        
        bar_a = self.barsArray[index_a]
        bar_b = self.barsArray[index_b]
        
        bar_a.move_to_index(index_a, index_b)
        bar_b.move_to_index(index_b, index_a)
        
        self.barsArray[index_a], self.barsArray[index_b] = self.barsArray[index_b], self.barsArray[index_a]
        
        return True
    
    def is_animating(self):
        return any(bar.is_animating() for bar in self.barsArray)