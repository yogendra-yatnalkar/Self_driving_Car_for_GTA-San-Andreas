import os
import numpy as np 
import tensorflow as tf
import numpy as np
import cv2
import efficientnet.tfkeras
import time
import pydirectinput

from preprocess.edge_highlighter import edge_highlighter
from capture_data.keyboard_capture import ScreenCapture
from capture_data.utility import Utility

def check_tf():
    print(tf.__version__)
    print('\n\n\nIs there a GPU available: ',tf.test.is_gpu_available(),'\n\n\n')

check_tf()

class PredictImage():

    def __init__(self, img_height, img_width, model_path, model_name):
        self.img_height = img_height
        self.img_width = img_width
        self.class_map = {0: 'backward', 1: 'backward_left', 2: 'backward_right', 3: 'forward',
                          4: 'forward_left', 5: 'forward_right', 6: 'left', 7: 'right'}
        self.action_map = {'backward': ['s'], 'backward_left': ['a','s'], 'backward_right': ['d','s'],
                           'forward': ['w'], 'forward_left': ['a','w'], 'forward_right': ['d','w'], 
                           'left': ['a'], 'right': ['d']}
        self.model = tf.keras.models.load_model(os.path.join(model_path,model_name))
    
    def predict(self, img):
        img = edge_highlighter(img)
        img = cv2.resize(img, (self.img_height, self.img_width),interpolation = cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img/255.
        img = np.expand_dims(img,axis = 0)
        ans = self.model.predict(img)
        ans = self.class_map[np.argmax(ans)]
        print(ans)
        action = self.action_map[ans]
        return action

if __name__ == "__main__":

    # Getting roi coordinates
    print(
        "\nDrag the mouse to the region which needs to be recorded and press enter...\nEnter 'c' to cancel!"
    )
    util = Utility()
    try:
        x0, y0, x1, y1 = util.get_coordinates()  # returns 4 coordinates
        if x0 == 0 and y0 == 0 and x1 == 0 and y0 == 0:
            sys.exit("ROI not selected")
    except BaseException as error:
        print("\nLog : ", error)
        print(
            "The Region of Intrest was not selected properly. Please rerun the program\n"
        )
        sys.exit()

    # initializing screen capture object and prediction object
    sc_cap = ScreenCapture(x0,y0,x1,y1)

    model_name = 'val_model_medium.h5'
    model_path = 'D:/Yogendra D/Self_driving_Car_for_GTA-San-Andreas/src/models'
    loaded_model = PredictImage(224,224,model_path,model_name)

    frame_skipper = 2
    action_history,action = [],[]
    try:
        while(True):
            # if(frame_skipper == 2):
            img = sc_cap.image_grab()
            # frame_skipper = 1
            
            action = loaded_model.predict(img)
            print(action)
            print('\n')

            for key in action_history:
                pydirectinput.keyUp(key)
            for key in action:
                pydirectinput.keyDown(key)
            action_history = action
            # time.sleep(0.3)
            # for key in action:
            #     pydirectinput.keyUp(key)
                
                # # display input frame
                # cv2.namedWindow('current window', cv2.WINDOW_NORMAL)
                # cv2.imshow('current window', img)
                # cv2.resizeWindow('current window', 300, 300)
            # else:
            #     frame_skipper += 1


            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    except KeyboardInterrupt:
        pass