"""
    This file is used to run the GreenMinds-Recycling-Bot
    to run in console: "python main_app.py"
"""

import tkinter as tk
import json
import os
import sys
import cv2
from PIL import Image, ImageTk
from tkinter_widgets.green_minds_model import GreenMindsModel
from tkinter_widgets.robot_bart import RobotBart
from tkinter_widgets.webcam_widget import WebcamWidget
from tkinter_widgets.button_widget import ButtonWidget


class TKinterApp:
    """
        Class used to create TKinter GUI
        shows the webcam where the user can take a picture and run inference,
        to see if it is recyclebel or not
    """

    def __init__(self):
        # Creates the layout for the app using tkinter
        self.root = tk.Tk()
        self._setup_layout()

        # instantiates the NN
        self.green_minds_model = GreenMindsModel(os.path.join(sys.path[0], "assets/checkpoint.pth"))

        # loads the json file that contains data for all of the objects
        with open(os.path.join(sys.path[0], "assets/items.json"), "r") as json_file:
            self.items = json.load(json_file)

        # starts the app
        self.root.mainloop()

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
                                         img_correct="b",
                                         img_wrong="c",
                                         command=lambda: (self._button_clicked("trash")))

        self.recycle_button = ButtonWidget(self.root, relwidth=.2, relheight=.1, relx=.05, rely=.96, anchor="sw",
                                           img_default="assets/gui/btn_recycle.png",
                                           img_correct="b",
                                           img_wrong="c",
                                           command=lambda: (self._button_clicked("recyclable")))

        self.compost_button = ButtonWidget(self.root, relwidth=.2, relheight=.1, relx=.95, rely=.96, anchor="se",
                                           img_default="assets/gui/btn_compost.png",
                                           img_correct="b",
                                           img_wrong="c",
                                           command=lambda: (self._button_clicked("compostable")))

        # needs to be last, the loop will break the flow
        self.webcam = WebcamWidget(self.root)

    def _button_clicked(self, recycling_type):
        """Runs inferences on the webcam image using the NN model
           Then will it respond if the user was correct
        """
        self.webcam.stop_webcam()
        frame = self.webcam.get_frame()

        # converts the color and parses it to pil image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)

        # makes the NN predict the type
        model_prediction = self.green_minds_model.predict(im_pil, topk=1)

        prediction_name = model_prediction[1][0]
        prediction_procent = model_prediction[0][0]

        print(prediction_procent, prediction_name)
        if prediction_procent < .5:
            self.show_popup_for(2000,
                                "Please try to align in middle of camera",
                                "if you are having continuos problems please ask for help",
                                self.webcam.panel_video)
            return

        if recycling_type == "recyclable":  # the user things that it is recyclebel
            if self.items["items"][prediction_name]["recycling-type"] == "recyclable":  # and it is recyclebel
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_correct_title"],
                                    self.items["items"][prediction_name]["guessed_correct_body"],
                                    self.webcam.panel_video)
            else:  # and it is not recyclebel
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_incorrect_title"],
                                    self.items["items"][prediction_name]["guessed_incorrect_body"],
                                    self.webcam.panel_video)
        elif recycling_type == "trash":  # code runs if the user belives it is trash
            if self.items["items"][prediction_name]["recycling-type"] == "trash":  # and it is trash
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_correct_title"],
                                    self.items["items"][prediction_name]["guessed_correct_body"],
                                    self.webcam.panel_video)
            else:  # and it is not trash
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_incorrect_title"],
                                    self.items["items"][prediction_name]["guessed_incorrect_body"],
                                    self.webcam.panel_video)
        else:  # code runs if the user things the item is compostable
            if self.items["items"][prediction_name]["recycling-type"] == "compostable":  # and it is compostable
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_correct_title"],
                                    self.items["items"][prediction_name]["guessed_correct_body"],
                                    self.webcam.panel_video)
            else:  # and it is not compostable
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_incorrect_title"],
                                    self.items["items"][prediction_name]["guessed_incorrect_body"],
                                    self.webcam.panel_video)

    def show_popup_for(self, milliseconds, title_text, body_text, root):
        """
            Creates popup frame that congratulates / says the user is wrong
            with there prediction of the object being recyclebel

        Arguments:
            milliseconds {int} -- amount of milliseconds before window is destroyed
            title {string} -- The title to be displayed
            root {tk} -- the window that the popup should be created in
        """
        self.webcam.add_text_title(title_text, milliseconds)
        self.webcam.add_text_body(body_text, milliseconds)

        # needs to be a lambda so else will it execute to early
        self.webcam.panel_video.after(milliseconds, lambda: self.webcam.start_webcam())


if __name__ == "__main__":
    TKinterApp()
