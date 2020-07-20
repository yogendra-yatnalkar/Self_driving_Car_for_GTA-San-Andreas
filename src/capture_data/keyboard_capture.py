import sys
import os
import cv2
from PIL import ImageGrab
import numpy as np
import pandas as pd
from pynput import keyboard
import uuid


class ScreenCapture:
    def __init__(self, x_ul, y_ul, x_br, y_br):
        # x_ul, y_ul --> x,y coordinates of upper left corner
        # x_br, y_br --> x,y coordinates of bottom right corner
        self.x_ul = x_ul
        self.y_ul = y_ul
        self.x_br = x_br    
        self.y_br = y_br

    def image_grab(self):
        screen = np.array(
            ImageGrab.grab(bbox=(self.x_ul, self.y_ul, self.x_br, self.y_br))
        )
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        return screen


class SaveFile:
    def __init__(self, path):
        self.path = path  # directory path where the image needs to be saved
        self.height = 700
        self.width = 700

    def get_image_name(self):
        img_name = str(uuid.uuid4().hex) + ".jpg"
        return img_name

    def set_dimensions(self, ht, wt):
        self.height = ht
        self.width = wt

    def save_image(self, image_np_array):  # numpy array of the image to be saved
        image_name = self.get_image_name()
        cv2.resize(image_np_array, (self.width, self.height))
        cv2.imwrite(os.path.join(self.path, image_name), image_np_array)
        return image_name

    def display_image(self, image_name, image_np_array):
        cv2.namedWindow(image_name, cv2.WINDOW_NORMAL)
        cv2.imshow(image_name, image_np_array)
        # cv2.resizeWindow(image_name, 400, 400)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            cv2.destroyAllWindows()

    def save_df(self, pd_df):  # pd_df --> pandas dataframe
        save_df_path = os.path.dirname(self.path)
        # storing to the parent folder of images
        pd_df.to_csv(os.path.join(save_df_path, "temp.csv"), index=False)
        # save the in-memory df to csv


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
        self.thresh = 10  # set threshold when same key is pressed continiously
        self.cnt = 0
        self.hist_key = (
            None  # Store the last pressed key to count the no of uuids a key is pressed
        )

    def set_thresh(self, thresh_val):
        self.thresh = thresh_val

    def on_press(self, key):
        if self.hist_key == key:
            self.cnt += 1
        else:
            self.cnt = 0
        if self.cnt >= self.thresh:
            self.count_flag = 0
        else:
            self.count_flag = 1
        self.hist_key = key
        if self.count_flag == 0:
            print(
                "\nKey not recorded because same key pressed for",
                self.thresh,
                "times...",
            )

        if key != keyboard.Key.esc:
            if key == keyboard.Key.alt_r:
                if self.pause_flag == 1:
                    self.pause_flag = 0
                else:
                    self.pause_flag = 1
            if self.pause_flag == 0:
                print("\nRecording Paused. Press alt(right) to continue...")
            if (
                self.count_flag == 1
                and self.pause_flag == 1
                and key != keyboard.Key.alt_r
            ):
                print("\nKey recorded. Press alt(right) to pause recording...")
                self.key_pressed.add(key)
                sc_grab = self.sc_cap_obj.image_grab()  # screen grab
                img_name = self.sv_file_obj.save_image(
                    sc_grab
                )  # save the screen to disk
                key_pressed_list = list(self.key_pressed)
                self.data_set.append(
                    {"image_name": img_name, "action": key_pressed_list}
                )
                key_pressed_list = []
                print(img_name, self.key_pressed)
                

    def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listener
            data_set_df = pd.DataFrame(self.data_set, columns=["image_name", "action"])
            self.sv_file_obj.save_df(data_set_df)
            return False
        if key in self.key_pressed:
            self.key_pressed.remove(key)
