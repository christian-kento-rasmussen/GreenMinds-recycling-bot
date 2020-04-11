"""
    This file is used to run the GreenMinds-Recycling-Bot
    to run in console: "python main_app.py"
"""

import tkinter as tk
import json
import os
import sys
from tkinter_widgets.robot_bart import RobotBart
from tkinter_widgets.webcam_widget import WebcamWidget
from tkinter_widgets.button_widget import ButtonWidget
from tkinter_widgets.object_detection import ObjectDetection


class TKinterApp:
    """
        Class used to create TKinter GUI
        shows the webcam where the user can take a picture and run inference,
        to see if it is recyclebel or not
    """

    def __init__(self):
        # Creates the layout for the app using tkinter
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._setup_layout()
        # starts the CNN to look for objects through the webcam
        self.object_detection = ObjectDetection(self._object_detected)

        # loads the json file that contains the data for all of the objects
        with open(os.path.join(sys.path[0], "assets/items.json"), "r") as json_file:
            self.items = json.load(json_file)

        # Holds the value of the object detected by the camera
        # if the string is not empty does it mean that an item is selected
        # if it is empty does it mean that the state of the came is 'looking for item'
        self.detection_name = ""

        # starts the app
        self.root.mainloop()

    def _on_close(self):
        """Stops the thread that runs the CNN
        """
        self.object_detection.stop()
        self.root.destroy()

    def _setup_layout(self):
        """Creates the layout for the app using tkinter
        """
        # sets up the view
        self.root.title("GreenMinds - Recycling app")
        self.root.geometry("1422x800")
        self.root.configure()
        # self.root.resizable(False, False)

        # creates bart and the background
        self.robot_bart = RobotBart(self.root)

        # creates the view for the buttons about recyclable, trash, and compostable
        self.trash_button = ButtonWidget(self.root, relwidth=.2, relheight=0.1, relx=.5, rely=.96, anchor="s",
                                         img_default="assets/gui/btn_waste.png",
                                         img_correct="assets/gui/btn_waste_correct.png",
                                         img_wrong="assets/gui/btn_waste_wrong.png",
                                         command=lambda: (self._button_clicked("trash")))

        self.recycle_button = ButtonWidget(self.root, relwidth=.2, relheight=.1, relx=.05, rely=.96, anchor="sw",
                                           img_default="assets/gui/btn_recycle.png",
                                           img_correct="assets/gui/btn_recycle_correct.png",
                                           img_wrong="assets/gui/btn_recycle_wrong.png",
                                           command=lambda: (self._button_clicked("recyclable")))

        self.compost_button = ButtonWidget(self.root, relwidth=.2, relheight=.1, relx=.95, rely=.96, anchor="se",
                                           img_default="assets/gui/btn_compost.png",
                                           img_correct="assets/gui/btn_compost_correct.png",
                                           img_wrong="assets/gui/btn_compost_wrong.png",
                                           command=lambda: (self._button_clicked("compostable")))

        # needs to be last, the loop will break the flow
        self.webcam = WebcamWidget(self.root)

    def _object_detected(self, detection_name):
        """Runs when an object have been placed in front of the camera

        Arguments:
            detection_name {str} -- The name of the item detected
        """
        self.object_detection.pause()
        self.webcam.stop_webcam()
        self.detection_name = detection_name
        self.webcam.add_text_title("Please select where this item belongs")
        self.robot_bart.make_bart_curious(self.items["items"][detection_name]["name"])

        # waits for button press / guess from user

    def _button_clicked(self, recycling_type):
        """ Checks if the user guessed correctly or not and response appropriately
            if no item hav been detected will it tell the user to put an item up to the camera
        """

        if self.detection_name == "":
            self.webcam.add_text_title("Please put an item up to the webcam before selecting a category", 2000)
            return

        if recycling_type == "recyclable":  # the user thinks that it is recyclebel
            if self.items["items"][self.detection_name]["recycling-type"] == "recyclable":  # and it is recyclebel
                self.recycle_button.change_image_correct()
                self.robot_bart.make_bart_happy()
                self.webcam.clear_text()
                self.webcam.add_text_title(self.items["items"][self.detection_name]["guessed_correct_title"])
                self.webcam.add_text_body(self.items["items"][self.detection_name]["guessed_correct_body"])
                self.compost_button.btn.after(3500, lambda: self._reset_app_after())

            else:  # and it is not recyclebel
                self.recycle_button.change_image_wrong()
                self.robot_bart.make_bart_sad()
                self.webcam.clear_text()
                self.webcam.add_text_title(self.items["items"][self.detection_name]["guessed_incorrect_title"])
                self.webcam.add_text_body(self.items["items"][self.detection_name]["guessed_incorrect_body"])

        elif recycling_type == "trash":  # code runs if the user belives it is trash
            if self.items["items"][self.detection_name]["recycling-type"] == "trash":  # and it is trash
                self.trash_button.change_image_correct()
                self.robot_bart.make_bart_happy()
                self.webcam.clear_text()
                self.webcam.add_text_title(self.items["items"][self.detection_name]["guessed_correct_title"])
                self.webcam.add_text_body(self.items["items"][self.detection_name]["guessed_correct_body"])
                self.trash_button.btn.after(3500, lambda: self._reset_app_after())

            else:  # and it is not trash
                self.trash_button.change_image_wrong()
                self.robot_bart.make_bart_sad()
                self.webcam.clear_text()
                self.webcam.add_text_title(self.items["items"][self.detection_name]["guessed_incorrect_title"])
                self.webcam.add_text_body(self.items["items"][self.detection_name]["guessed_incorrect_body"])

        else:  # code runs if the user things the item is compostable
            if self.items["items"][self.detection_name]["recycling-type"] == "compostable":  # and it is compostable
                self.compost_button.change_image_correct()
                self.robot_bart.make_bart_happy()
                self.webcam.clear_text()
                self.webcam.add_text_title(self.items["items"][self.detection_name]["guessed_correct_title"])
                self.webcam.add_text_body(self.items["items"][self.detection_name]["guessed_correct_body"])
                self.compost_button.btn.after(3500, lambda: self._reset_app_after())
            else:  # and it is not compostable
                self.compost_button.change_image_wrong()
                self.robot_bart.make_bart_sad()
                self.webcam.clear_text()
                self.webcam.add_text_title(self.items["items"][self.detection_name]["guessed_incorrect_title"])
                self.webcam.add_text_body(self.items["items"][self.detection_name]["guessed_incorrect_body"])

    def _reset_app_after(self):
        self.detection_name = ""
        self.webcam.clear_text()
        self.robot_bart.make_bart_default()
        self.recycle_button.change_image_default()
        self.trash_button.change_image_default()
        self.compost_button.change_image_default()
        self.webcam.start_webcam()
        self.object_detection.resume()


if __name__ == "__main__":
    TKinterApp()
