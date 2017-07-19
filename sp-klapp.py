import shytlight_simulator as shytlight
import time
import cv2
import numpy as np
import threading

class KlappPattern(threading.Thread):
    def __init__(self):
        super(KlappPattern, self).__init__()

        self.stopping = False

        self.base_color = (0x44, 0x64, 0x55) # stromboli
        # self.base_color = (0x0, 0x0, 0x0)
        self.highlight_color = (0xfd, 0xd2, 0x62) # cream can
        self.pi = 3.14
        self.bpm = 124.

    def stop(self):
        self.stopping = True

    def run(self):
        while(self.stopping == False):
            self.tpf = int(1/(bpm/4.)*60./100.*122.)
        for i in range(50):
          for j in range(100):
            # create image on large basis
            circles = np.zeros((50,80, 3), np.uint8)
            circles[:,:]= np.flipud(self.base_color) # numpy ordering is reversed, BGR
            # draw a line
            endpoint = ((np.sin(pi*j/50.)*1000+80).astype(np.int),(np.cos(pi*j/50.)*1000+50).astype(np.int))
            inv_endpoint = ((np.sin(pi*j/50.)*-1000+80).astype(np.int),(np.cos(pi*j/50.)*-1000+50).astype(np.int))
            if (j>=0) and (j<25):
                startp = (0,0)
            if (j>=25) and (j<50):
                startp = (80, 0)
            if (j>= 50) and (j<75):
                startp = (80,50)
            if (j>=75):
                startp = (0, 50)
            cv2.line(circles, (startp), (endpoint), self.highlight_color, 10)
            cv2.line(circles, (startp), (inv_endpoint), self.highlight_color, 10)
            # blur circle
            bl_circles = cv2.blur(circles, (11,11))
            # resize image to our real led size
            test_geometry = cv2.resize(bl_circles,(8,5))
            # add frame to buffer
            shytlight.add_frame(self.tpf, test_geometry)

