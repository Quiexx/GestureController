# GestureController
An application that recognizes gestures using a webcam and allows you to control your computer using gestures.

Authors: Lvov Andrey, Baryshev Andrey

---
![Teaser gif](./docs/app_demostration.gif)

## Usage

---
### Install python 3.9  
https://www.python.org/downloads/release/python-390/

### Install dependencies
```shell
pip install kivy opencv-python torch pyautogui numpy mediapipe pillow
```

### Run app
```shell
python src\app\app.py
```

---
### Camera action group
*Open* - turn camera on.

*Close* - turn camera off.

*Change* - switch to another camera

*Show camera* - turn on/off camera displaying

### Hands action group

*Show hands* - turn on/off hand landmarks displaying

### Gesture control action group

*Show gesture* - turn on/off recognised gesture displaying

---
## Gestures

0: Open palm  
Action: Open / close task bar  
![Open palm](./src/icons/gesture/open_palm.jpg)

1: Index finger up  
Action: Left mouse button click  
![Index finger up](./src/icons/gesture/index_up.jpg)

2: Fist  
Action: None  
![Fist](./src/icons/gesture/fist.jpg)

3: Thumb aside  
Action: Go to the previous tab (ctrl + shift + tab or left arrow if task bar is opened)  
![Thumb aside](./src/icons/gesture/thumb_aside.jpg)

4: Pinky aside  
Action: Go to the next tab (ctrl + tab or right arrow if task bar is opened)  
![Pinky aside](./src/icons/gesture/pinky_aside.jpg)

5: Index and middle fingers up  
Action: Cursor control  
![Index and middle fingers up](./src/icons/gesture/index_middle_up.jpg)

6: Thumb up  
Action: None  
![Thumb up](./src/icons/gesture/thumb_up.jpg)

7: Thumb and index fingers separated  
Action: None  
![Thumb and index fingers separated](./src/icons/gesture/thumb_index_separated.jpg)

8: Thumb and index fingers together  
Action: None  
![Thumb and index fingers together](./src/icons/gesture/thumb_index_together.jpg)
