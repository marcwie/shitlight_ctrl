import threading
import shytlight_simulator as shytlight
import numpy as np
from palettable import wesanderson


class RaindropPattern(threading.Thread):

    def __init__(self, n_rows=5, n_led=8):
        super(RaindropPattern, self).__init__()

        self.stopping = False

        self.n_led = n_led
        self.n_rows = n_rows
        colors = wesanderson.Zissou_5.colors
        self.colors = colors
        self.n_colors = len(colors)


    def random_color(self):
        """Pick a color from the colormap at random."""
        current_color = self.colors[np.random.randint(self.n_colors)]
        while np.mean(current_color) < 64:
            current_color = self.colors[np.random.randint(self.n_colors)]
        return current_color


    def raindrops(self, current_color):
        brightness = np.zeros((self.n_rows, self.n_led, 3))
        is_drop = np.zeros((self.n_rows, self.n_led)) 

        n_drops = 0 
        while (not ((n_drops == 100) and (brightness == 0).all()) and (self.stopping == False)):
            where_drop = np.where(is_drop)

            brightness[where_drop] = current_color

            is_drop[where_drop] = 0
            rows, leds = where_drop[0], where_drop[1]
            mask = leds < self.n_led - 1
            rows = rows[mask]
            leds = leds[mask] + 1
            where_drop = (rows, leds) 
            is_drop[where_drop] = 1

            if ((np.random.random() < 0.10) or (brightness == 0).all()) and (n_drops < 100):
                random_row = np.random.randint(self.n_rows)
                if (is_drop[random_row, :2] == 0).all():
                    is_drop[random_row, 0] = 1
                    n_drops += 1 

            for __ in range(4):
                brightness[brightness > 0] -= np.log10(brightness[brightness > 0])
                shytlight.add_frame(rep=1, frame=brightness)
                brightness[brightness < 1.5] = 0
 
    
    def run(self):
        current_color = self.random_color()
        while(self.stopping == False):
            current_color = self.random_color()
            self.raindrops(current_color)

    def stop(self):
        self.stopping = True
