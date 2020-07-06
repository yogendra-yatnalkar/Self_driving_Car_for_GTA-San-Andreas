import os
import numpy as np
import cv2
from pyautogui import screenshot
import time
import pandas as pd

class Utility:

    def generate_delay(self, delay_time):
        for i in range(delay_time,0,-1):
            print("Program will start in : ",i)
            time.sleep(1)

    def get_coordinates(self):
        screen = np.array(screenshot())
        screen = cv2.cvtColor(screen,cv2.COLOR_RGB2BGR)
        # roi = cv2.selectROI(screen)
        x0, y0, w, h = cv2.selectROI(screen) 
        #returns the top-left corner coordinates and the width and height of the roi
        cv2.destroyAllWindows()
        x1 = x0 + w
        y1 = y0 + h
        return (x0,y0,x1,y1)

    def delete_temp_files(self, ds_list, ds_path): 
        #only delete images and csv which are created in the current session of the program
        if(os.path.exists(ds_path)):
            files = set(os.listdir(ds_path))
            for img in ds_list:
                img_name = img['image_name']
                if(img_name in files):
                    os.remove(os.path.join(ds_path,img_name))
                    print(img_name," - Deleted")
            csv_save_path = os.path.dirname(ds_path)
            # Also delete temp.csv if created
            files = set(os.listdir(csv_save_path))
            if('temp.csv' in files):
                os.remove(os.path.join(csv_save_path, 'temp.csv'))
                print("temp.csv - Deleted")
        else:
            print("Path does not exist")

    # func to merge temp.csv with dataset.csv
    def merge_temp_ds(self, ds_path): 
        csv_save_path = os.path.dirname(ds_path) # csv files are stored in parent folder of dataset folder
        df_temp = pd.read_csv(os.path.join(csv_save_path, 'temp.csv'))  # data_fram of temp.csv
        df_ds = pd.read_csv(os.path.join(csv_save_path, 'dataset.csv')) # data_frame of dataset.csv
        df_ds = df_ds.append(df_temp, sort = False) 
        print('Two CSV files merged')

        # Saving the merged data_frame
        df_ds.to_csv(os.path.join(csv_save_path, 'dataset.csv'), index = False)
        print('Dataset.csv Saved')

        # Deleting the temp.csv
        files = set(os.listdir(csv_save_path))
        if('temp.csv' in files):
            os.remove(os.path.join(csv_save_path, 'temp.csv'))
            print("temp.csv - Deleted")
            