import shytlight_simulator as shytlight
import time
import cv2
import numpy as np
import threading

class CirclePattern(threading.Thread):
    def __init__(self):
        super(CirclePattern, self).__init__()
        self.stopping = False
        self.color = (0, 255, 0)
    def stop(self):
        self.stopping = True

    def run(self):
        while (self.stopping == False):
            for j in range(200):
              # create image on large basis
              circles = np.zeros((50,80,3))
              # draw a circle with increasing radius
              cv2.circle(circles, (40,25), j*2, self.color, 8)
              # blur circle
              bl_circles = cv2.blur(circles, (21,21))
              # resize image to our real led size
              test_geometry = cv2.resize(bl_circles,(8,5))
              # add frame to buffer
              shytlight.add_frame(1, test_geometry)

