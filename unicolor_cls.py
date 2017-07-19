import threading
import shytlight_simulator as shytlight
import numpy as np
from palettable import wesanderson


class UnicolorPattern(threading.Thread):

    def __init__(self, n_rows=5, n_led=8):
        super(UnicolorPattern, self).__init__()

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


    def unicolor(self, current_color):
        brightness = np.zeros((self.n_rows, self.n_led, 3))
        brightness[:, :] = current_color

        new_color = self.random_color()
        while new_color == current_color:
            new_color = self.random_color()

        transitions = np.array(new_color) - np.array(current_color)
        red_transition = np.linspace(0, transitions[0], 50)
        green_transition = np.linspace(0, transitions[1], 50)
        blue_transition = np.linspace(0, transitions[2], 50)

        for _ in range(50):
            brightness[:, :, 0] = current_color[0] + red_transition[_]
            brightness[:, :, 1] = current_color[1] + green_transition[_]
            brightness[:, :, 2] = current_color[2] + blue_transition[_]
            shytlight.add_frame(rep=4, frame=brightness)
            
        current_color = new_color

        return current_color

    
    def run(self):
        current_color = self.random_color()
        
        while(self.stopping == False):
            current_color = self.unicolor(current_color)


    def stop(self):
        self.stopping = True
