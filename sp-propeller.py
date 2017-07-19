import shytlight_simulator as shytlight
import time
import cv2
import numpy as np
import threading

class PropellerPattern(threading.Thread):
    def __init__(self):
        super(PropelerPattern, self).__init__()

        self.stopping = False

        self.base_color = (0x44, 0x64, 0x55) # stromboli
        self.base_color = (0x0, 0x0, 0x0)
        self.highlight_color = (0xfd, 0xd2, 0x62) # cream can
        
        self.bpm = 124.

    def stop(self):
	self.stopping = True

    def run(self):
        while(self.stopping == False):
            self.tlp = int(1/(bpm/4.)*60./100.*122.)
            for j in range(100):
                # create image on large basis
                circles = np.zeros((50,80, 3), np.uint8)
                circles[:,:]= np.flipud(self.base_color) # numpy ordering is reversed, BGR
                # draw a line
                endpoint = ((np.sin(np.pi*j/50)*100+40).astype(np.int),(np.cos(np.pi*j/50)*100+25).astype(np.int))
                inv_endpoint = ((np.sin(np.pi*j/50)*-100+40).astype(np.int),(np.cos(np.pi*j/50)*-100+25).astype(np.int))
                cv2.line(circles, (40,25), (endpoint), self.highlight_color, 8)
                cv2.line(circles, (40,25), (inv_endpoint), self.highlight_color, 8)
                # blur circle
                bl_circles = cv2.blur(circles, (11,11))
                # resize image to our real led size
                test_geometry = cv2.resize(bl_circles,(8,5))[::,:,:]
                # add frame to buffer
                shytlight.add_frame(2, test_geometry)

