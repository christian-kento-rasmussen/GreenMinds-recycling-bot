"""
    This file is used to run the GreenMinds-Recycling-Bot
    to run in console: "python tkinter_app.py"
"""

import tkinter as tk
import json
import os
import sys
import cv2
from PIL import Image, ImageTk
from green_minds_model import GreenMindsModel


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
        #self.root.bind("<Configure>", self._update_layout)

        # instantiates the NN
        self.green_minds_model = GreenMindsModel(os.path.join(sys.path[0], "assets/model/checkpoint.pth"))

        # loads the json file that contains data for all of the objects
        with open(os.path.join(sys.path[0], "items.json"), "r") as json_file:
            self.items = json.load(json_file)

        # initiating camera and starts the app
        self.camera = cv2.VideoCapture(0)
        self.camera1()
        self.root.mainloop()

    def _setup_layout(self):
        """
            Creates the layout for the app using tkinter
        """
        # sets up the view
        self.root.title("GreenMinds - Recycling app")
        self.root.geometry("1422x800")
        self.root.configure(background="#1bcc00")
        # self.root.resizable(False, False)

        # creates the bg
        self.bg = tk.Label(self.root)
        self.bg.place(relwidth=1, relheight=1)
        self.bg.update()
        self.bg_image_orig = Image.open("assets/gui/bg.png")
        self.bg_image = self.bg_image_orig.resize((self.bg.winfo_width(), self.bg.winfo_height()), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg.configure(image=self.bg_image)
        self.bg.image = self.bg_image

        # creates the test label for use later
        self.response_label_title = tk.Label(self.root)
        self.response_label_body = tk.Label(self.root)

        # creates the view for the camera
        self.panel_video = tk.Label(self.root)
        self.panel_video.place(relx=.95, rely=0.45, relwidth=.4, relheight=.65, anchor="e")

        # creates the view for the buttons about recyclable, trash, and compostable
        self.trash_button = tk.Button(self.root, command=lambda: (self._button_clicked("trash")))
        self.trash_button.place(relwidth=.2, relheight=.1, relx=.5, rely=.96, anchor="s")
        self.trash_button.update()
        self.trash_button_image_orig = Image.open("assets/gui/btn_waste.png")
        self.trash_button_image = self.trash_button_image_orig.resize((self.trash_button.winfo_width(), self.trash_button.winfo_height()), Image.ANTIALIAS)
        self.trash_button_image = ImageTk.PhotoImage(self.trash_button_image)
        self.trash_button.configure(image=self.trash_button_image)

        self.recycle_button = tk.Button(self.root, command=lambda: self._button_clicked("recyclable"))
        self.recycle_button.place(relwidth=.2, relheight=.1, relx=.05, rely=.96, anchor="sw")
        self.recycle_button.update()
        self.recycle_button_image_orig = Image.open("assets/gui/btn_recycle.png")
        self.recycle_button_image = self.recycle_button_image_orig.resize((self.recycle_button.winfo_width(), self.recycle_button.winfo_height()), Image.ANTIALIAS)
        self.recycle_button_image = ImageTk.PhotoImage(self.recycle_button_image)
        self.recycle_button.configure(image=self.recycle_button_image)

        self.compostable_button = tk.Button(self.root, command=lambda: self._button_clicked("compostable"))
        self.compostable_button.place(relwidth=.2, relheight=.1, relx=.95, rely=.96, anchor="se")
        self.compostable_button.update()
        self.compostable_button_image_orig = Image.open("assets/gui/btn_compost.png")
        self.compostable_button_image = self.compostable_button_image_orig.resize((self.compostable_button.winfo_width(), self.compostable_button.winfo_height()), Image.ANTIALIAS)
        self.compostable_button_image = ImageTk.PhotoImage(self.compostable_button_image)
        self.compostable_button.configure(image=self.compostable_button_image)

    def _update_layout(self, event):
        self.bg.update()
        bg_image = self.bg_image_orig.resize((self.bg.winfo_width(), self.bg.winfo_height()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(bg_image)
        self.bg.configure(image=bg_image)
        self.bg.image = bg_image

    def camera1(self):
        """
            Updates camera with new image from webcam
        """
        _, frame = self.camera.read()
        # flips the image
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        self.panel_video.configure(image=frame)
        self.panel_video.image = frame
        self.panel_video.after(1, self.camera1)

    def _button_clicked(self, recycling_type):
        """
            runs inferences on the webcam image using the NN model
            Then will it respond if the user was correct
        """

        frame = self.camera.read()[1]

        # converts the color and parses it to pil image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)

        # makes the NN predict the type
        model_prediction = self.green_minds_model.predict(im_pil, topk=1)

        prediction_name = model_prediction[1][0]
        prediction_procent = model_prediction[0][0]

        print(prediction_procent, prediction_name)
        if prediction_procent < .5:
            self.show_popup_for(2000, "Please try to align in middle of camera", "if you are having continuos problems please ask for help", self.panel_video)
            return

        if recycling_type == "recyclable":  # the user things that it is recyclebel
            if self.items["items"][prediction_name]["recycling-type"] == "recyclable":  # and it is recyclebel
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_correct_title"],
                                    self.items["items"][prediction_name]["guessed_correct_body"],
                                    self.panel_video)
            else:  # and it is not recyclebel
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_incorrect_title"],
                                    self.items["items"][prediction_name]["guessed_incorrect_body"],
                                    self.panel_video)
        elif recycling_type == "trash":  # code runs if the user belives it is trash
            if self.items["items"][prediction_name]["recycling-type"] == "trash":  # and it is trash
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_correct_title"],
                                    self.items["items"][prediction_name]["guessed_correct_body"],
                                    self.panel_video)
            else:  # and it is not trash
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_incorrect_title"],
                                    self.items["items"][prediction_name]["guessed_incorrect_body"],
                                    self.panel_video)
        else:  # code runs if the user things the item is compostable
            if self.items["items"][prediction_name]["recycling-type"] == "compostable":  # and it is compostable
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_correct_title"],
                                    self.items["items"][prediction_name]["guessed_correct_body"],
                                    self.panel_video)
            else:  # and it is not compostable
                self.show_popup_for(5000,
                                    self.items["items"][prediction_name]["guessed_incorrect_title"],
                                    self.items["items"][prediction_name]["guessed_incorrect_body"],
                                    self.panel_video)

    def show_popup_for(self, milliseconds, title_text, body_text, root):
        """
            Creates popup frame that congratulates / says the user is wrong
            with there prediction of the object being recyclebel

        Arguments:
            milliseconds {[int]} -- [amount of milliseconds before window is destroyed]
            title {[string]} -- [The title to be displayed]
            root {[tk]} -- [the window that the popup should be created in]
        """
        # Creates the response text
        self.response_label_title = tk.Label(root, text=title_text, font=('Courier', 27), wraplength=500, pady=20)
        self.response_label_title.place(relx=0, rely=0, relwidth=1, relheight=.3, anchor="nw")

        self.response_label_body = tk.Label(root, text=body_text, font=('Courier', 20), wraplength=500, justify=tk.LEFT, padx=20)
        self.response_label_body.config(anchor=tk.NW)
        self.response_label_body.place(relx=0, rely=.3, relwidth=1, relheight=.7, anchor="nw")

        self.response_label_title.after(milliseconds, self.response_label_title.destroy)
        self.response_label_body.after(milliseconds, self.response_label_body.destroy)


if __name__ == "__main__":
    TKinterApp()
