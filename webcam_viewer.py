"""This file is used to create a simple webcam viewer
    to use run: python webcam_viewer.py
"""

import argparse
import time
from cv2 import cv2

def main():
    '''
        shows the view of the webcam in a popup screen
        press esc to exit program
    '''

    # set up our command line arguments
    parser = argparse.ArgumentParser(description='Shows the webcam using cv2')
    parser.add_argument('--webcam_number', type=int, default=0, help='Select what camera to use')
    # gets our arguments from the command line
    in_arg = parser.parse_args()
    cam = cv2.VideoCapture(in_arg.webcam_number)
    
    while True:
        # reads the camera
        _, img = cam.read()

        # flips the image
        img = cv2.flip(img, 1)

        # shows it to the viewer in a pop up window
        cv2.imshow('my webcam', img)

        # breaks the loop when the user presses esc
        if cv2.waitKey(1) == 27: 
            break  # esc to quit

    cv2.destroyAllWindows()

# Call to main function to run the program
if __name__ == "__main__":
    start = time.time()
    main()
    print("execution time:", time.time() - start)