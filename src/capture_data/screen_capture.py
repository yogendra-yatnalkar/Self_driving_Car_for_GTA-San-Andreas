import cv2
from PIL import ImageGrab
import numpy as np

class ScreenCapture:

    def __init__(self, x_ul, y_ul, x_br, y_br): 
        self.x_ul = x_ul
        self.y_ul = y_ul
        self.x_br = x_br
        self.y_br = y_br

    def image_grab(self):
        screen =  np.array(ImageGrab.grab(bbox=(self.x_ul,self.y_ul,self.x_br,self.y_br)))
        screen = cv2.cvtColor(screen,cv2.COLOR_RGB2BGR)
        return screen
