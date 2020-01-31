# Green Minds Recycling bot
Green Minds Recycling bot is an object detection script that uses a CNN to identify different objects,
The script is used to make an interactive guide for children to learn what can be recycled and what can't. By making them pick up items and bring them to the camera and saying if it is recyclable or not.
Then will an on-screen robot congratulate them if they are correct.

For more information about Green Minds visit the [website](http://www.green-minds.org/)

# Scripts
## webcam_recorder.py
It is used to record data for training of the CNN, by taking pictures from the camera at a specified interval and save them to a folder.

## GreenMindsNN.ipynb
It is used to train the CNN in an interactive environment before deployment.