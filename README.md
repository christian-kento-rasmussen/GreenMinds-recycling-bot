# Green Minds Recycling bot
Green Minds Recycling bot is an object detection program that uses a CNN to identify different objects.
The program is used to make an interactive guide for children to learn what can be recycled and what can't. By making them pick up items and bringing them to the camera and saying if it is recyclable or not.
Then will an on-screen robot congratulate them if they are correct.

For more information about Green Minds visit the [website](http://www.green-minds.org/)

[![<Rasmussen-Christian>](https://circleci.com/gh/Rasmussen-Christian/GreenMinds-recycling-bot.svg?style=svg)](https://circleci.com/gh/Rasmussen-Christian/GreenMinds-recycling-bot)

# Usage
To start the program make sure dependencies are installed by running `pip install -r requirements.txt`. Then open the main app by running `python tkinter_app.py assets/model/checkpoint.pth`.
From here can you place a supported object in front of the camera and guess if it is recyclable or not, afterwards will the program tell if you were correct.

# Scripts
## tkinter_app.py
[tkinter_app.py](tkinter_app.py) is the main file in the program which, when run using `python tkinter_app.py assets/model/checkpoint.pth` will open a tkinter window that will display the webcam and buttons to say if the item placed in the view of the webcam is recyclable. After the user guesses if it is recyclable, will the program use the CNN to recognize the object and say the if the user was right.

## GreenMindsNN.ipynb
[GreenMindsNN.ipynb](GreenMindsNN.ipynb) is used to train the neural network using either your own machine or [colab.google.com](https://colab.research.google.com/) which can train the NN in the cloud for free. The trained NN will then be saved and is currently places for the [tkinter_app.py](tkinter_app.py) script to use at `assets/model/checkpoint.pth`

## green_minds_model.py
[green_minds_model.py](green_minds_model.py) is used to load a pre-trained CNN PyTorch model and run inference on PIL images, this class is used as a backend for [tkinter_app.py](tkinter_app.py)
