import threading
import shytlight_simulator as shytlight
import numpy as np
from palettable import wesanderson


class CrossPattern(threading.Thread):

    def __init__(self, n_rows=5, n_led=8):
        super(CrossPattern, self).__init__()
        self.stopping = False
        self.n_rows = n_rows
        self.n_led = n_led

        colors = wesanderson.Zissou_5.colors

        self.colors = colors
        self.n_colors = len(colors)


    def random_color(self):
        """Pick a color from the colormap at random."""
        current_color = self.colors[np.random.randint(self.n_colors)]
        while np.mean(current_color) < 64:
            current_color = self.colors[np.random.randint(self.n_colors)]
        return current_color


    def one_flash(self, current_color):
        random_row = np.random.randint(self.n_rows)
        random_led = np.random.randint(self.n_led)
        brightness = np.zeros((5, 8, 3))
        brightness[random_row, random_led, :] = current_color

        offset = 0
        decreasing = False
        while not decreasing:
            decreasing = True
            rep = 1
            if random_row + offset < self.n_rows:
                brightness[random_row+offset, random_led, :] = current_color
                rep = 5
                decreasing = False
           
            if random_row - offset >= 0:
                brightness[random_row-offset, random_led, :] = current_color
                rep = 5
                decreasing = False

            if random_led + offset < self.n_led:
                brightness[random_row, random_led+offset, :] = current_color
                rep = 5
                decreasing = False

            if random_led - offset >= 0:
                brightness[random_row, random_led-offset, :] = current_color
                rep = 5
                decreasing = False

            for _ in range(rep):
                shytlight.add_frame(rep=1, frame=brightness)
                brightness[brightness > 0] -= np.log10(brightness[brightness > 0])
                brightness[brightness < 10] = 0

            offset += 1

        while (brightness > 0).any():
            rep = 1
            if random_row + offset < self.n_rows and offset >= 0:
                brightness[random_row+offset, random_led, :] = current_color
                rep = 5
           
            if random_row - offset >= 0 and offset >= 0:
                brightness[random_row-offset, random_led, :] = current_color
                rep = 5

            if random_led + offset < self.n_led and offset >= 0:
                brightness[random_row, random_led+offset, :] = current_color
                rep = 5

            if random_led - offset >= 0 and offset >= 0:
                brightness[random_row, random_led-offset, :] = current_color
                rep = 5

            for _ in range(rep):
                shytlight.add_frame(rep=1, frame=brightness)
                brightness[brightness > 0] -= np.log10(brightness[brightness > 0])
                brightness[brightness < 10] = 0

            offset -= 1


    def run(self):
        current_color = self.random_color()
        
        while(self.stopping == False):
            if np.random.random() < 0.1:
                current_color = self.random_color()
        
            self.one_flash(current_color)


    def stop(self):
        self.stopping = True
