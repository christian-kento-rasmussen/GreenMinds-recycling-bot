"""File used to capture images from webcam
"""

import argparse
import time
import sys
from pathlib import Path
from PIL import Image
import numpy as np
from cv2 import cv2
from torchvision import transforms


def main():
    '''
    Takes pictures at a certain interval from the camera and saves it to a folder
    '''

    # set up our command line arguments
    parser = argparse.ArgumentParser(description='Takes photos at a given interval')
    parser.add_argument('save_dir', type=str, help='Select directory to save pictures in')
    parser.add_argument('--photos_count', '-pc', type=int, default=5, help='Amount of photos to take')
    parser.add_argument('--delay', '-d', type=float, default=.5, help='Delay between each image being taken')
    parser.add_argument('--camera', '-c', type=int, default=0, help='Select what camera to use')
    parser.add_argument('--start_val', '-sv', type=int, default=0, help='Set the start value for the naming of the images, so not to overide images already taken')
    parser.add_argument('--resize', '-r', type=int, help='what size should the image be resized to')
    # gets our arguments from the command line
    in_arg = parser.parse_args()

    # Sets up webcam
    webcam = cv2.VideoCapture(in_arg.camera)

    # creates the dir where the photos will be stored if it does not exist
    Path(in_arg.save_dir).mkdir(parents=True, exist_ok=True)

    # creates the pre proccessing transforms used for flag --scale
    resize = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(255)
    ])

    for i in range(in_arg.photos_count):
        try:
            progress_bar(i + 1, in_arg.photos_count)

            # reads the webcam
            frame = webcam.read()[1]

            # resizes the image if specified
            if (in_arg.resize is not None):
                frame = resize(Image.fromarray(frame))
                frame = np.asarray(frame)

            # saves image
            cv2.imwrite("{}/image_{}.jpg".format(in_arg.save_dir, i + in_arg.start_val), frame)

        except(KeyboardInterrupt):
            webcam.release()
            cv2.destroyAllWindows()

        time.sleep(in_arg.delay)

    # releases the camera
    webcam.release()
    cv2.destroyAllWindows()
    print("Camera off.")


def progress_bar(value, endvalue, bar_length=20):
    """Creates a simple progress bar
       based on: https://stackoverflow.com/a/37630397/6688026

    Arguments:
        value {float} -- current progress from 0
        endvalue {float} -- max value

    Keyword Arguments:
        bar_length {int} -- length of the bar in terminal (default: {20})
    """
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rProgress: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


# Call to main function to run the program
if __name__ == "__main__":
    start = time.time()
    main()
    print("execution time:", time.time() - start)
