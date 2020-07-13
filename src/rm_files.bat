@ECHO OFF
D:
cd "Yogendra D\Self_driving_Car_for_GTA-San-Andreas\src"
rm dataset.csv
ECHO dataset.csv deleted

cd csv_dataset
rm *.jpg
ECHO Deleted all the images from csv_dataset

cd ..\tf_dataset
ECHO into tf_dataset

cd forward\
ECHO into forward
rm *.jpg

cd ..\backward
ECHO into backward
rm *.jpg

cd ..\left
ECHO into left
rm *.jpg

cd ..\right
ECHO into right
rm *.jpg

cd ..\forward_left
ECHO into forward_left
rm *.jpg

cd ..\forward_right
ECHO into forward right
rm *.jpg

cd ..\backward_left
echo into backward left
rm *.jpg

cd ..\backward_right
echo into backward right
rm *.jpg

cd ..\..\other
ECHO into other
python dataset_csv_template.py
echo dataset.csv created