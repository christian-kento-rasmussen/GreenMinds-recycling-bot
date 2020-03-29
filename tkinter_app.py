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
        self.setup_layout()

        # instantiates the NN
        self.green_minds_model = GreenMindsModel(os.path.join(sys.path[0], "assets/model/checkpoint.pth"))
        
        # loads the json file that contains data for all of the objects
        with open(os.path.join(sys.path[0], "items.json"), "r") as json_file:
            self.items = json.load(json_file)

        # initiating camera and the gui
        self.camera = cv2.VideoCapture(0)
        self.camera1()
        self.root.mainloop()

    def setup_layout(self):
        """
            Creates the layout for the app using tkinter
        """
        # sets up the view
        self.root = tk.Tk()
        self.root.title("GreenMinds - Recycling app")
        self.root.geometry("1422x800")
        self.root.configure(background="#1bcc00")
        self.root.resizable(False, False)

        # creates the bg
        self.bg_image = ImageTk.PhotoImage(Image.open("assets/gui/root_bg.png"))
        self.bg = tk.Label(self.root, image=self.bg_image)
        self.bg.place(relwidth=1, relheight=1)

        # creates the title bar
        self.title_image = ImageTk.PhotoImage(Image.open("assets/gui/GreenMinds_title.png"))
        self.title_bg = tk.Label(self.root, image=self.title_image)
        self.title_bg.place(width=750, height=75, anchor="n", relx=.5, rely=.035)

        # creates the view for the camera
        self.camera_bg_image = ImageTk.PhotoImage(Image.open("assets/gui/camera_bg.png"))
        self.camera_bg = tk.Label(self.root, image=self.camera_bg_image)
        self.camera_bg.place(width=800, height=450, relx=.5, anchor="n", y=150)
        self.panel_video = tk.Label(self.camera_bg)
        self.panel_video.place(relx=.5, rely=0.075, relwidth=.9, relheight=.8, anchor="n")

        # creates the view for the buttons about recyclable, trash, and compostable
        self.trash_button_image = ImageTk.PhotoImage(Image.open("assets/gui/btn_not_recyclable.png"))
        self.trash_button = tk.Button(self.root, image=self.trash_button_image, command=lambda: (self.button_clicked("trash")))
        self.trash_button.place(width=380, height=98, relx=.3, rely=.96, anchor="s")
        self.recycle_button_image = ImageTk.PhotoImage(Image.open("assets/gui/btn_is_recyclable.png"))
        self.recycle_button = tk.Button(self.root, image=self.recycle_button_image, command=lambda: self.button_clicked("recyclable"))
        self.recycle_button.place(width=380, height=98, relx=.7, rely=.96, anchor="s")
        self.compostable_button_image = ImageTk.PhotoImage(Image.open("assets/gui/btn_is_recyclable.png"))
        self.compostable_button = tk.Button(self.root, image=self.compostable_button_image, command=lambda: self.button_clicked("compostable"))
        self.compostable_button.place(width=380, height=98, relx=.0, rely=.96, anchor="s")

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

    def button_clicked(self, recycling_type):
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
        if prediction_procent < .2:
            self.show_popup_for(2000, "Please try to align in middle of camera", self.root)
            return

        if recycling_type == "recyclable":  # the user things that it is recyclebel
            if self.items["items"][prediction_name]["recycling-type"] == "recyclable":  # and it is recyclebel
                self.show_popup_for(3000, self.items["items"][prediction_name]["guessed_correct"], self.root)
            else:  # and it is not recyclebel
                self.show_popup_for(3000, self.items["items"][prediction_name]["guessed_incorrect"], self.root)
        elif recycling_type == "trash":  # code runs if the user belives it is trash
            if self.items["items"][prediction_name]["recycling-type"] == "trash":  # and it is trash
                self.show_popup_for(3000, self.items["items"][prediction_name]["guessed_correct"], self.root)
            else:  # and it is not trash
                self.show_popup_for(3000, self.items["items"][prediction_name]["guessed_incorrect"], self.root)
        else: # code runs if the user things the item is compostable
            if self.items["items"][prediction_name]["recycling-type"] == "compostable":  # and it is compostable
                self.show_popup_for(3000, self.items["items"][prediction_name]["guessed_correct"], self.root)
            else:  # and it is not compostable
                self.show_popup_for(3000, self.items["items"][prediction_name]["guessed_incorrect"], self.root)

    def show_popup_for(self, milliseconds, message, root):
        """
            Creates popup frame that congratulates / says the user is wrong
            with there prediction of the object being recyclebel
        
        Arguments:
            milliseconds {[int]} -- [amount of milliseconds before window is destroyed]
            message {[string]} -- [The message to be displayed]
            root {[tk]} -- [the window that the popup should be created in]
        """
        # creates the popup frame and label
        self.popup_bg_image = ImageTk.PhotoImage(Image.open("assets/gui/popup_bg.png"))
        self.popup_bg = tk.Label(root, image=self.popup_bg_image)
        self.popup_bg.place(width=432, height=432, relx=.5, y=160, anchor="n")

        self.popup_text = tk.Label(self.popup_bg, text=message, font=("Courier", 30), wraplength=300, bg="#e5e5e5")
        self.popup_text.place(relx=0.5, rely=.1, relwidth=0.8, relheight=0.9, anchor="n")

        # destroys it again after the message have been read
        self.popup_bg.after(milliseconds, self.popup_bg.destroy)


if __name__ == "__main__":
    TKinterApp()
