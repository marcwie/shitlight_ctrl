#!/usr/bin/env python3



import os
import sys
import time
import random

from PyQt5 import QtGui


import shitlight_simulator



light = shitlight_simulator.Light()


img = QtGui.QImage('s.ppm')


rgb_colors = [(0,0,0)] * 64

# get RGB values from image into array
for x in range(8):
    for y in range(8):
        rgb_colors[x*8+y] = QtGui.QColor(img.pixel(x,y)).getRgb()[:3]


light.set_color(rgb_colors)

