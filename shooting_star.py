#!/usr/bin/env python3



import time
import random

import shitlight_simulator



light = shitlight_simulator.Light()



chance = .001


colors = [0] * 64
rgb_colors = [(0,0,0)] * 64

while True:
    for i, color in enumerate(colors):
        if random.random() < chance:
            colors[i] = 255
            rgb_colors[i] = ((color),) * 3
        elif color > 0:
            colors[i] -= 1
            rgb_colors[i] = ((color),) * 3
    light.set_color(rgb_colors)
    time.sleep(0.02)

