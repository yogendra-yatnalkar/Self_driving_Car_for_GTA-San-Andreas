# Dataset compatible to tf.data
import pandas as pd
import os

csv_path = 'D:/Yogendra D/Self_driving_Car_for_GTA-San-Andreas/src'
csv_file_name = 'dataset.csv'
df = pd.read_csv(os.path.join(csv_path,csv_file_name))
directions = {'w':'forward','s':'backward','a':'left','d':'right','aw':'forward_left','dw':'forward_right','as':'backward_left','ds':'backward_right'}
print(df)
for i in range(len(df)):
    action = df['action'][i].replace('[','').replace(']','').replace(',','').replace("'",'').replace(" ",'')
    action = ''.join(sorted(action))
    print('\n',i,action,end = " : ")
    accepted = ['w','a','s','d','aw','dw','as','ds']

    if(action not in accepted):
        print('delete')

    print(directions[action])
    

