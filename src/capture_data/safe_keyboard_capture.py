''' Note: ScreenCapture and SaveImage class will be integrated in this file. '''

from pynput import keyboard
import time
import pandas as pd
from save_file import SaveFile
from screen_capture import ScreenCapture

# Future utility packages
from pyautogui import screenshot
import numpy as np
import cv2
import os

class KeyboardCapture:

    def __init__(self, x_ul, y_ul, x_br, y_br, save_path):
        # x_ul, y_ul --> x,y coordinates of upper left corner
        # x_br, y_br --> x,y coordinates of bottom right corner
        self.key_pressed = set()
        # action_df --> DataFrame where image and the action will be saved. Conver later to .csv
        self.action_df = pd.DataFrame(columns=['image_name','action'])
        self.sc_cap_obj = ScreenCapture(x_ul, y_ul, x_br, y_br)
        # sc_cap_obj --> screen capture object
        self.sv_file_obj = SaveFile(save_path) 
        self.save_path = save_path
        # sv_file_obj --> save file object

    def on_press(self, key):
        self.key_pressed.add(key)
        sc_grab = self.sc_cap_obj.image_grab() # screen grab
        img_name = self.sv_file_obj.save_image(sc_grab)  # save the screen to disk
        
        last_row = len(self.action_df)
        print(self.action_df)
        print(last_row)
        self.action_df.loc[len(self.action_df)] = [img_name,self.key_pressed]
        print(img_name,self.key_pressed)

    def on_release(self,key):
        if(key == keyboard.Key.esc):
            # Stop listener
            self.sv_file_obj.save_df(self.action_df)
            return False
        if(key in self.key_pressed):
            self.key_pressed.remove(key)

def get_coordinates():
    screen = np.array(screenshot())
    screen = cv2.cvtColor(screen,cv2.COLOR_RGB2BGR)
    # roi = cv2.selectROI(screen)
    x0, y0, w, h = cv2.selectROI(screen) 
    #returns the top-left corner coordinates and the width and height of the roi
    cv2.destroyAllWindows()
    x1 = x0 + w
    y1 = y0 + h
    return (x0,y0,x1,y1)

if __name__ == "__main__":
    start_time = time.time()
    x0,y0,x1,y1 = get_coordinates()

    # The module will start after a delay of 10 sec
    for i in range(4,0,-1):
        print("The program will start in : ",i)
        time.sleep(1)

    save_img_path = 'D:/Yogendra D/AI_for_any_game_using_CNN/src/game_dataset'
    obj = KeyboardCapture(x0,y0,x1,y1,save_img_path)

    try:
        listener = keyboard.Listener(
        on_press=obj.on_press,
        on_release=obj.on_release)
        listener.run()
    except BaseException as error:
        print("Unexpected error : ",error)
    
    end_time = time.time()
    print("Time required for execution : ", end_time - start_time)