#!/usr/bin/env python3



import time
import random

import shitlight_simulator



light = shitlight_simulator.Light()



chance = .001


colors = [0] * 64
rgb_colors = [(0,0,0)] * 64



while True:
    for i in range(2):
        for j in range(8):
            for k in range(8):
                colors[j*8+k] = (i+j+k)%2
        light.set_color([ (x*255,x*255,0) for x in colors])
        time.sleep(1)

