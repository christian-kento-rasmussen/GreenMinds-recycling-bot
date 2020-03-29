"""This file is used to create a simple webcam viewer
    to use run: python webcam_viewer.py
"""

import argparse
import time
import numpy as np
from cv2 import cv2
from PIL import Image
from torchvision import transforms


def main():
    ''' Shows the view of the webcam in a popup screen
        press esc to exit program
    '''
    # set up our command line arguments
    parser = argparse.ArgumentParser(description='Shows the webcam using cv2')
    parser.add_argument('--webcam_number', '-wn', type=int, default=0, help='Select what camera to use')
    parser.add_argument('--format_as_ImageNet', '-fai', dest='format_as_ImageNet', action='store_true', help='Should the webcamview be formatted as a ImageNet trained model would see it')
    # gets our arguments from the command line
    in_arg = parser.parse_args()

    # activates the webcam
    cam = cv2.VideoCapture(in_arg.webcam_number)

    # creates the pre proccessing transforms used for flag --format_as_ImageNet
    resize = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224)
    ])

    while True:
        # reads the camera
        img = cam.read()[1]

        # flips the image
        img = cv2.flip(img, 1)

        # cuts the image as an ImageNet trained CNN would see it, if --format_as_ImageNet==true
        if (in_arg.format_as_ImageNet):
            img = resize(Image.fromarray(img))
            img = np.asarray(img)

        # shows it to the viewer in a pop up window
        cv2.imshow('webcam feed', img)

        # breaks the loop when the user presses esc
        if cv2.waitKey(1) == 27:
            break  # esc to quit

    cv2.destroyAllWindows()


# Call to main function to run the program
if __name__ == "__main__":
    start = time.time()
    main()
    print("execution time:", time.time() - start)
