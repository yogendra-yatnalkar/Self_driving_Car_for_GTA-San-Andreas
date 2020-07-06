import os
import cv2
import time

class SaveFile:

    def __init__(self, path):
        self.path = path # directory path where the image needs to be saved
        self.height = 700
        self.width = 700

    def get_image_name(self):
        files_list = os.listdir(self.path)
        dir_len = len(files_list)
        files_list = []
        img_name = str(dir_len + 1) + '.jpg'
        return img_name

    def set_dimensions(self,ht,wt):
        self.height = ht
        self.width = wt
    
    def save_image(self, image_np_array): # numpy array of the image to be saved
        image_name = self.get_image_name()
        cv2.resize(image_np_array, (self.width, self.height))
        cv2.imwrite(os.path.join(self.path, image_name), image_np_array)
        return image_name

    def display_image(self,image_name, image_np_array):
        cv2.namedWindow(image_name,cv2.WINDOW_NORMAL)
        cv2.imshow(image_name, image_np_array)
        # cv2.resizeWindow(image_name, 400, 400)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def save_df(self, pd_df): # pd_df --> pandas dataframe
        save_df_path = os.path.dirname(self.path) 
        # storing to the parent folder of images
        pd_df.to_csv(os.path.join(save_df_path, 'temp.csv'), index = False)
            # save the in-memory df to csv
