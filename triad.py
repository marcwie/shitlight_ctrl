#!/usr/bin/env python3



import time
import random

import shitlight_simulator



light = shitlight_simulator.Light()


chance = 0.01

triad = [ (255, 0, 180), (180, 250, 0), (0, 180, 255) ]

rgb_colors = [(0,0,0)] * 64

while True:
    for i in range(64):
        if random.random() < chance:
            rgb_colors[i] = random.choice(triad)
    light.set_color(rgb_colors)
    time.sleep(0.02)

