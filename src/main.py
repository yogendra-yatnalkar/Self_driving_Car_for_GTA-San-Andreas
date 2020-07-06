import time
from pynput import keyboard
from capture_data.utility import Utility
from capture_data.keyboard_capture import KeyboardCapture
from preprocess.remove_duplicate import RemoveDuplicate
import gc
import sys

def main():
    while(input("Press 's' to start the program: ") != 's'):
        time.sleep(0.1)
    print('\nDrag the mouse to the region which needs to be selected and press enter...\n')
    util = Utility()
    try:
        x0,y0,x1,y1 = util.get_coordinates() #returns 4 coordinates
        if(x0 == 0 and y0 ==0 and x1 == 0 and y0 == 0):
            sys.exit("ROI not selected")  
    except BaseException as error:
        print("\nLog : ", error)
        print('The Region of Intrest was not selected properly. Please rerun the program\n')
        sys.exit()

    # The module will start after a defined dalay
    delay_time = 6
    util.generate_delay(delay_time)
    start_time = time.time()
    save_img_path = 'D:/Yogendra D/AI_for_any_game_using_CNN/src/game_dataset' 
    # csv files will be stores one directory above the image path
    obj = KeyboardCapture(x0,y0,x1,y1,save_img_path)

    try:
        listener = keyboard.Listener(
        on_press=obj.on_press,
        on_release=obj.on_release)
        listener.run()
        # merge current dataset with original dataset and delete current file
        util.merge_temp_ds(obj.save_path) 
    except BaseException as error:
        print("Unexpected error : ",error)
        print("The current created dataset will be cleared")
        util.delete_temp_files(obj.data_set, obj.save_path)
        obj.data_set = []
        gc.collect()
    
    ds_path = 'D:/Yogendra D/AI_for_any_game_using_CNN/src/game_dataset' 
    csv_path = 'D:/Yogendra D/AI_for_any_game_using_CNN/src'
    rm_obj = RemoveDuplicate(ds_path)
    rm_obj.rm_duplicate_img()

    end_time = time.time()
    print("Time required for execution : ", end_time - start_time)

if __name__ == "__main__":
    main()