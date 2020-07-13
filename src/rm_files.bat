@ECHO OFF
D:
cd "Yogendra D\Self_driving_Car_for_GTA-San-Andreas\src"
rm dataset.csv
cd csv_dataset
rm *

cd ..
cd tf_dataset

cd forward
rm *
cd ..

cd backward
rm *
cd ..

cd left
rm *
cd ..

cd right
rm *
cd ..

cd forward_left
rm *
cd ..

cd forward_right
rm *
cd ..

cd backward_left
rm *
cd ..

cd backward_right
rm *

cd "Yogendra D\Self_driving_Car_for_GTA-San-Andreas\src"
cd other
python dataset_csv_template.py