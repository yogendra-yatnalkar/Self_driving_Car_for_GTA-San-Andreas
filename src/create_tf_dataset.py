# Dataset compatible to tf.data
import pandas as pd
import os
import shutil

ds_path = "D:/Yogendra D/Self_driving_Car_for_GTA-San-Andreas/src/csv_dataset"
csv_path = "D:/Yogendra D/Self_driving_Car_for_GTA-San-Andreas/src"
csv_file_name = "dataset.csv"
tf_ds_path = "D:/Yogendra D/Self_driving_Car_for_GTA-San-Andreas/src/tf_dataset"

df = pd.read_csv(os.path.join(csv_path, csv_file_name))
accepted = ["w", "a", "s", "d", "aw", "dw", "as", "ds"]
directions = {
    "w": "forward",
    "s": "backward",
    "a": "left",
    "d": "right",
    "aw": "forward_left",
    "dw": "forward_right",
    "as": "backward_left",
    "ds": "backward_right",
}
print(df)
for i in range(len(df)):
    action = (
        df["action"][i]
        .replace("[", "")
        .replace("]", "")
        .replace(",", "")
        .replace("'", "")
        .replace(" ", "")
    )
    action = "".join(sorted(action))
    print("\n", i, action, end=" : ")
    img_name = df["image_name"][i]

    if action not in accepted:
        print("\n\n--------------delete\n\n")
        print("Removed :: ", end=" ")
        print(img_name, df["action"][i])
        df.drop(i, axis=0, inplace=True)
        os.remove(os.path.join(ds_path, img_name))
    else:
        print(directions[action])
        direction_folder = directions[action]
        dest_path = os.path.join(tf_ds_path,direction_folder)
        print(dest_path)
        shutil.copy(os.path.join(ds_path, img_name), dest_path)


df.to_csv(os.path.join(csv_path, "dataset.csv"), index=False)

