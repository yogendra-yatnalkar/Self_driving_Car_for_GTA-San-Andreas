## Self-Driving car for Grand Theft Auto: San Andreas

---

**Important Links**

- Youtube: https://youtu.be/om3HvgN1s00

- Kaggle Dataset Used for training:
    1. https://www.kaggle.com/yogendrayatnalkar/gtasanandreas-drivingtiny
    2. https://www.kaggle.com/yogendrayatnalkar/gta-san-andreas-medium-size

- Kaggle Kernel where model was trained: https://www.kaggle.com/yogendrayatnalkar/fork-of-self-driving-starter

(Please show some love on Github, Youtube and Kaggle if you liked this project)

---

Installation:
1. Git clone this repository
2. Run the following command:
> pip install -r requirements.txt
3. Download the model and start using the project within your game (see further instrctions below)

---

How to use this model:
1. Download the model from above kaggle kernel (https://www.kaggle.com/yogendrayatnalkar/fork-of-self-driving-starter) and save it in the ./src/models/ folder. 
2. Rename the model to: val_model_medium.h5
3. Start GTA San Andreas in window mode (i.e not in full screen)
-- Not: to start the game in window mode you will need "d3d9.dll" file to be in the installation folder of the game. I have attached the required dll in this repository itself. 
4. Open command prompt and inside src folder. (Make sure the all the requirement.txt is installed)
5. Run the command:- 
> python play.py
6. Follow the insturctions on the command prompt now.




