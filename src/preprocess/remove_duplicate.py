from PIL import Image
import imagehash
import os
import pandas as pd

class RemoveDuplicate:
    
    def __init__(self,img_ds_path, csv_file_path = None, csv_file_name = 'dataset.csv'):
        self.img_ds_path = img_ds_path
        self.hash_db = set()
        self.count_duplicate = 0
        self.count_corrupt = 0
        if(csv_file_path == None):
            self.csv_file_path = os.path.dirname(img_ds_path) 
        else:
            self.csv_file_path = csv_file_path
        self.csv_file_name = csv_file_name

    def rm_duplicate_img(self):
        if(os.path.exists(self.csv_file_path)):
            ds_df = pd.read_csv(os.path.join(self.csv_file_path,self.csv_file_name))
            if(os.path.exists(self.img_ds_path)):
                img_db = os.listdir(self.img_ds_path)

                for i in range(len(ds_df['image_name'])):
                    img_name = ds_df['image_name'][i]

                    if(img_name not in img_db):
                        # print('\n',ds_df['image_name'].iloc[i],ds_df['action'].iloc[i], '--- REMOVED from csv file---' ,'\n')
                        print('\n Index : ',i ,'--- REMOVED from csv file---\n')

                        ds_df.drop(i, axis=0, inplace = True)
                        self.count_corrupt += 1
                    else:
                        img = Image.open(os.path.join(self.img_ds_path,img_name))
                        hash = imagehash.phash(img)
                        if(hash in self.hash_db):
                            os.remove(os.path.join(self.img_ds_path,img_name))
                            ds_df.drop(i, axis=0, inplace = True)
                            print('\n',img_name, '--- REMOVED from dataset and csv file ---','\n')
                            self.count_duplicate += 1
                        else:
                            self.hash_db.add(hash)
                            print('Checked: ',img_name)
                        img = None
                        img_db.remove(img_name)

                if(len(img_db) != 0):
                    for img_name in img_db:
                        os.remove(os.path.join(self.img_ds_path,img_name))
                        print('\n',img_name, '--- REMOVED from dataset ---','\n')

                print('\n"No. of corrupted csv entries found and deleted : ',self.count_corrupt)
                print('\n"No. of duplicate images found and deleted : ',self.count_duplicate)
                print('\nNo of unaccounted files : ',len(img_db))

                ds_df.to_csv(os.path.join(self.csv_file_path,'dataset.csv'), index = False)
                print('\nUpdated CSV file saved\n')
            else:
                print("Image DataSet Path do not exist")
        else:
            print("CSV file path do not exist")
