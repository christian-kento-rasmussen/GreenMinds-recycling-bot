"""Code for continuous object detection
"""
import threading
import os
import sys
import cv2
from PIL import Image
from tkinter_widgets.green_minds_model import GreenMindsModel


class ObjectDetection(threading.Thread):
    """Class runs in thread and looks continuously for recognized object to appear in webcam view
    """

    def __init__(self, callback_command, checkpoint_path="assets/checkpoint.pth", webcam_number=0):
        """
        Arguments:
            callback_command {function} -- The command to be called when the NN detects an object

        Keyword Arguments:
            checkpoint_path {str} -- the path to the NN checkpoint (default: {"assets/checkpoint.pth"})
            webcam_number {int} -- the webcam number to use (default: {0})
        """
        threading.Thread.__init__(self)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

        self.checkpoint_path = checkpoint_path
        self.webcam_number = webcam_number
        self.callback_command = callback_command

        self.start()

    def pause(self):
        """Pauses the CNN from detection objects
        """
        self.__flag.clear()   # set to False to allow threads to block

    def resume(self):
        """Resumes the CNN to continue detecting objects
        """
        self.__flag.set()  # set to True to allow thread to stop blocking

    def stop(self):
        """Stops the thread
        """
        self.__flag.set()    # Restores a thread from a paused state.
        self.__running.clear()    # set to False

    def run(self):
        """Main loop looks for object in webcam view and calls callback_command on detection
        """
        # instantiates the NN and the camera
        green_minds_model = GreenMindsModel(os.path.join(sys.path[0], self.checkpoint_path))
        camera = cv2.VideoCapture(self.webcam_number)

        # runs continuous
        while self.__running.isSet():
            self.__flag.wait()

            # converts the webcam and parses it to pil image
            frame = camera.read()[1]
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)

            # makes the NN predict the type
            model_prediction = green_minds_model.predict(im_pil, topk=1)
            prediction_name = model_prediction[1][0]
            prediction_procent = model_prediction[0][0]

            print(prediction_procent)
            if prediction_procent > .6:
                self.callback_command(prediction_name)

        camera.release()
        print("INFO - thread stopped")
