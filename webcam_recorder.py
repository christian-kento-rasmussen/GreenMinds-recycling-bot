"""File used to capture images from webcam
"""

import argparse
import time
import sys
from pathlib import Path
from cv2 import cv2


def main():
    '''
    Takes pictures at a certain interval from the camera and saves it to a folder
    '''

    # set up our command line arguments
    parser = argparse.ArgumentParser(description='Takes photos at a given interval')
    parser.add_argument('save_dir', type=str, help='Select directory to save pictures in')
    parser.add_argument('--photos_count', type=int, default=5, help='Amount of photos to take')
    parser.add_argument('--delay', type=float, default=.5, help='Delay between each image being taken')
    parser.add_argument('--camera', type=int, default=0, help='Select what camera to use')
    parser.add_argument('--scale_percent', type=int, default=50, help='How much should the quality be scaled down, from 100 to 1 procent of original')
    parser.add_argument('--start_val', type=int, default=0, help='Set the start value for the naming of the images, so not to overide images already taken')
    # gets our arguments from the command line
    in_arg = parser.parse_args()

    # Sets up webcam
    webcam = cv2.VideoCapture(in_arg.camera)

    # creates the dir where the photos will be stored if it does not exist
    Path(in_arg.save_dir).mkdir(parents=True, exist_ok=True)

    for i in range(in_arg.photos_count):
        try:
            progress_bar(i + 1, in_arg.photos_count)

            frame = webcam.read()[1]
            cv2.imwrite("{}/image_{}.jpg".format(in_arg.save_dir, i + in_arg.start_val), frame)

            # resizes the image to save space
            img = cv2.imread("{}/image_{}.jpg".format(in_arg.save_dir, i + in_arg.start_val), cv2.IMREAD_UNCHANGED)
            scale_percent = in_arg.scale_percent  # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

            # saves image
            cv2.imwrite("{}/image_{}.jpg".format(in_arg.save_dir, i + in_arg.start_val), resized)

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
