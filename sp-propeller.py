import shytlight_simulator as shytlight
import time
import cv2
import numpy as np

# initialize threads
shytlight.init_shitlight()

# base_color = (0x44, 0x64, 0x55) # stromboli
base_color = (0x0, 0x0, 0x0)
highlight_color = (0xfd, 0xd2, 0x62) # cream can
pi = 3.14

for i in range(10):
  for j in range(100):
    # create image on large basis
    circles = np.zeros((500,800, 3), np.uint8)
    circles[:,:]= np.flipud(base_color) # numpy ordering is reversed, BGR
    # draw a line
    endpoint = ((np.sin(pi*j/50)*1000+400).astype(np.int),(np.cos(pi*j/50)*1000+250).astype(np.int))
    inv_endpoint = ((np.sin(pi*j/50)*-1000+400).astype(np.int),(np.cos(pi*j/50)*-1000+250).astype(np.int))
    cv2.line(circles, (400,250), (endpoint), highlight_color, 80)
    cv2.line(circles, (400,250), (inv_endpoint), highlight_color, 80)
    # blur circle
    bl_circles = cv2.blur(circles, (301,301))
    # resize image to our real led size
    test_geometry = cv2.resize(bl_circles,(8,5))
    # add frame to buffer
    shytlight.add_frame(1, test_geometry)

 
