''' Note: ScreenCapture and SaveImage class will be integrated in this file. '''
import sys
sys.path.append('D:/Yogendra D/AI_for_any_game_using_CNN/src/capture_data')

import pandas as pd
from save_file import SaveFile
from screen_capture import ScreenCapture

# should be in future main
from pynput import keyboard
from utility import Utility
import gc
import time

class KeyboardCapture:

    def __init__(self, x_ul, y_ul, x_br, y_br, save_path):
        # x_ul, y_ul --> x,y coordinates of upper left corner
        # x_br, y_br --> x,y coordinates of bottom right corner
        self.key_pressed = set()
        self.data_set = []
        self.sc_cap_obj = ScreenCapture(x_ul, y_ul, x_br, y_br)
        # sc_cap_obj --> screen capture object
        self.sv_file_obj = SaveFile(save_path) 
        # sv_file_obj --> save file object
        self.save_path = save_path

        self.pause_flag = 1 
        self.count_flag = 1  # decides the program will pause keyboard capture or not
        self.thresh = 8# set threshold when same key is pressed continiously
        self.cnt = 0
        self.hist_key = None # Store the last pressed key to count the no of times a key is pressed

    def set_thresh(self, thresh_val):
        self.thresh = thresh_val

    def on_press(self, key):
        if(self.hist_key == key):
            self.cnt += 1
        else:
            self.cnt = 0
        if(self.cnt >= self.thresh):
            self.count_flag = 0
        else:
            self.count_flag = 1
        self.hist_key = key
        print('\n',self.count_flag,end = ' ')

        if(key != keyboard.Key.esc):
            if(key == keyboard.Key.alt_r):
                if(self.pause_flag == 1):
                    self.pause_flag = 0
                else:
                    self.pause_flag = 1
            print(self.pause_flag)
            if(self.count_flag == 1 and self.pause_flag == 1 and key != keyboard.Key.alt_r):
                self.key_pressed.add(key)
                sc_grab = self.sc_cap_obj.image_grab() # screen grab
                img_name = self.sv_file_obj.save_image(sc_grab)  # save the screen to disk
                key_pressed_list = list(self.key_pressed)
                self.data_set.append({'image_name': img_name, 'action': key_pressed_list})
                key_pressed_list = []
                print(img_name, self.key_pressed)

    def on_release(self,key):
        if(key == keyboard.Key.esc):
            # Stop listener
            data_set_df = pd.DataFrame(self.data_set, columns = ['image_name','action']) 
            self.sv_file_obj.save_df(data_set_df)
            return False
        if(key in self.key_pressed):
            self.key_pressed.remove(key)
